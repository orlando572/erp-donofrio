from datetime import timedelta

from odoo import Command, fields
from odoo.tests import tagged

from .common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestOrdenesDeProduccion(DonofrioStockCase):
    """HU-14 (RF010): la OP reserva insumos por FEFO, crea el lote con vencimiento y calcula el costo."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plantilla = cls.env.ref('donofrio_base.pt_h01')
        cls.helado = cls.plantilla.product_variant_id
        cls.bom = cls.env.ref('donofrio_base.bom_pt_h01')
        cls.leche = cls._producto('in_leche')
        # Receta de 100 unidades: 4 kg pulpa, 3 kg azúcar, 1 kg glucosa, 10 L leche, 100 palitos, 100 envolturas
        cls.lotes_de_leche = {
            'proximo': cls._lote(cls.leche, 'LECHE-OP-PRONTO', 6),
            'lejano': cls._lote(cls.leche, 'LECHE-OP-LEJANO', 9),
        }
        for lote in cls.lotes_de_leche.values():
            cls._stock(cls.leche, lote, 8)
        for linea in cls.bom.bom_line_ids:
            insumo = linea.product_id
            if insumo == cls.leche:
                continue
            lote = cls._lote(insumo, f'{insumo.default_code}-OP', 300) if insumo.tracking == 'lot' else False
            cls._stock(insumo, lote, linea.product_qty * 10)

    def _orden(self, cantidad=100):
        orden = self.env['mrp.production'].create({
            'product_id': self.helado.id,
            'product_qty': cantidad,
            'bom_id': self.bom.id,
        })
        orden.action_confirm()
        orden.action_assign()
        return orden

    def _producir(self, orden, horas_por_operacion=1):
        orden.action_generate_serial()
        orden.qty_producing = orden.product_qty
        orden.move_raw_ids.picked = True
        ahora = fields.Datetime.now()
        for operacion in orden.workorder_ids:
            operacion.write({'time_ids': [Command.create({
                'workcenter_id': operacion.workcenter_id.id,
                'loss_id': self.env.ref('mrp.block_reason7').id,
                'date_start': ahora - timedelta(hours=horas_por_operacion),
                'date_end': ahora,
            })], 'state': 'done'})
        orden.with_context(skip_backorder=True).button_mark_done()
        return orden

    def test_valoracion_fifo_en_terminados_e_insumos(self):
        categorias = self.env['product.category'].search([('id', 'child_of', [
            self.env.ref('donofrio_base.cat_terminados').id, self.env.ref('donofrio_base.cat_insumos').id])])
        for categoria in categorias:
            with self.subTest(categoria=categoria.complete_name):
                self.assertEqual(categoria.property_cost_method, 'fifo')
                self.assertEqual(categoria.property_valuation, 'real_time')

    # --- Reserva de insumos ----------------------------------------------------------------------------

    def test_la_op_toma_los_componentes_de_la_receta(self):
        orden = self._orden()
        self.assertEqual(orden.state, 'confirmed')
        self.assertEqual(set(orden.move_raw_ids.product_id), set(self.bom.bom_line_ids.product_id))
        self.assertEqual(set(orden.move_raw_ids.mapped('state')), {'assigned'})
        self.assertEqual(len(orden.workorder_ids), 4)

    def test_la_op_reserva_los_insumos_por_fefo(self):
        orden = self._orden()
        movimiento = orden.move_raw_ids.filtered(lambda m: m.product_id == self.leche)
        reservado = {ml.lot_id: ml.quantity for ml in movimiento.move_line_ids}
        # La receta pide 10 L: salen 8 L del lote que vence antes y 2 L del siguiente
        self.assertEqual(reservado, {
            self.lotes_de_leche['proximo']: 8,
            self.lotes_de_leche['lejano']: 2,
        })

    # --- Producir: lote con vencimiento -----------------------------------------------------------------

    def test_al_producir_se_crea_el_lote_con_vencimiento(self):
        orden = self._producir(self._orden())

        self.assertEqual(orden.state, 'done')
        lote = orden.lot_producing_ids
        self.assertEqual(len(lote), 1)
        self.assertEqual(lote.product_id, self.helado)
        self.assertTrue(lote.expiration_date)
        dias = (lote.expiration_date - fields.Datetime.now()).days
        self.assertIn(dias, (364, 365), 'El helado vence a los 12 meses')
        self.assertEqual(self._disponible(self.helado, lote, orden.location_dest_id), 100)
        self.assertAlmostEqual(
            (lote.expiration_date - lote.alert_date).total_seconds(), timedelta(days=30).total_seconds(), delta=60)

    def test_producir_descuenta_los_insumos(self):
        self._producir(self._orden())
        for lote in self.lotes_de_leche.values():
            self.assertGreaterEqual(self._disponible(self.leche, lote), 0)
        total_leche = sum(self._disponible(self.leche, lote) for lote in self.lotes_de_leche.values())
        self.assertEqual(total_leche, 6)

    def test_el_lote_producido_sale_despues_por_fefo(self):
        """Lo producido entra al circuito: la entrega siguiente lo reserva por vencimiento."""
        orden = self._producir(self._orden())
        otro = self._lote(self.helado, 'H01-ANTIGUO', 40)
        self._stock(self.helado, otro, 20, orden.location_dest_id)
        entrega = self._picking(
            self.lim.pick_type_id, self.lim.lot_stock_id, self.lim.wh_output_stock_loc_id, self.helado, 15)
        entrega.action_assign()
        self.assertEqual(entrega.move_ids.move_line_ids.lot_id, otro)

    # --- Costo ----------------------------------------------------------------------------------------

    def test_se_calcula_el_costo_de_lo_producido(self):
        """Costo del lote = insumos consumidos + horas de cada centro de trabajo (4 operaciones × 1 h)."""
        orden = self._producir(self._orden())

        movimiento = orden.move_finished_ids.filtered(lambda m: m.product_id == self.helado)
        costo_insumos = sum(m.value for m in orden.move_raw_ids)
        costo_operaciones = sum(wo.workcenter_id.costs_hour * wo.duration / 60 for wo in orden.workorder_ids)
        self.assertGreater(costo_insumos, 0)
        self.assertGreater(costo_operaciones, 0)
        self.assertAlmostEqual(movimiento.value, costo_insumos + costo_operaciones, delta=0.05)
        self.assertAlmostEqual(movimiento.price_unit, (costo_insumos + costo_operaciones) / 100, delta=0.001)
        self.assertAlmostEqual(self.helado.standard_price, movimiento.price_unit, delta=0.001)

    def test_mas_horas_de_operacion_suben_el_costo(self):
        self._stock(self.leche, self._lote(self.leche, 'LECHE-OP-EXTRA', 8), 30)
        corta = self._producir(self._orden(), horas_por_operacion=1)
        larga = self._producir(self._orden(), horas_por_operacion=3)
        self.assertGreater(larga.move_finished_ids.price_unit, corta.move_finished_ids.price_unit)

    def test_una_tanda_completa_cuesta_menos_que_su_precio_de_venta(self):
        """La receta es una tanda industrial: el costo de las horas de línea se reparte entre miles de unidades."""
        for linea in self.bom.bom_line_ids:
            insumo = linea.product_id
            lote = self._lote(insumo, f'{insumo.default_code}-TANDA', 200) if insumo.tracking == 'lot' else False
            self._stock(insumo, lote, linea.product_qty * 1.1)
        orden = self._producir(self._orden(self.bom.product_qty))

        costo_unitario = orden.move_finished_ids.price_unit
        self.assertEqual(orden.qty_produced, 10000)
        self.assertGreater(costo_unitario, 0)
        self.assertLess(costo_unitario, self.plantilla.list_price)

    def test_producir_genera_asientos_de_valoracion(self):
        orden = self._producir(self._orden())
        for movimiento in orden.move_raw_ids | orden.move_finished_ids:
            with self.subTest(movimiento=movimiento.product_id.default_code):
                self.assertTrue(movimiento.account_move_id, 'Cada movimiento valorado debe tener su asiento')
        asiento = orden.move_finished_ids.account_move_id
        self.assertEqual(asiento.state, 'posted')
        self.assertEqual(asiento.amount_total, orden.move_finished_ids.value)
