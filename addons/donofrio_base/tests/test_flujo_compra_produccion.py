from datetime import timedelta

from odoo import Command, fields
from odoo.tests import tagged

from .common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestFlujoCompraProduccion(DonofrioStockCase):
    """HU-33 (parte de compras y producción): flujo de punta a punta con los datos reales del módulo.

    Compra de insumos (planificador mín./máx. u OC directa al proveedor de la ficha) → recepción con lote y
    vencimiento → OP de la receta de la paleta de fresa (reserva FEFO) → producir → lote del terminado con
    vencimiento → existencias, costo y asientos de valoración coherentes con lo que se pagó al proveedor.

    Los tests de ``test_recepcion_despacho``, ``test_reabastecimiento`` y ``test_produccion`` prueban cada tramo
    por separado (con stock puesto a mano); aquí el stock de la OP solo existe porque se compró y se recibió.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plantilla = cls.env.ref('donofrio_base.pt_h01')
        cls.helado = cls.plantilla.product_variant_id
        cls.bom = cls.env.ref('donofrio_base.bom_pt_h01')
        cls.leche = cls._producto('in_leche')
        cls.regla_leche = cls.env.ref('donofrio_base.rp_leche')
        cls.cantidad_op = 100   # la receta es de 10 000 unidades: una OP de 100 consume el 1 % de cada insumo

    # --- Utilidades ------------------------------------------------------------------------------------

    def _oc(self, insumo, cantidad):
        """OC en borrador al proveedor y al precio de la ficha del insumo."""
        tarifa = insumo.seller_ids[0]
        return self.env['purchase.order'].create({
            'partner_id': tarifa.partner_id.id,
            'order_line': [Command.create({
                'product_id': insumo.id,
                'product_qty': cantidad,
                'price_unit': tarifa.price,
            })],
        })

    def _recibir_oc(self, orden, lotes=None, cantidad=None, con_pendiente=False):
        """Recibe la OC en Lima. ``lotes`` = [(nombre, días para vencer, cantidad)] para insumos con lote.

        Con ``con_pendiente`` deja lo que falta en una entrega pendiente (backorder); si no, la cierra tal cual.
        """
        recepcion = orden.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
        self.assertEqual(len(recepcion), 1)
        movimiento = recepcion.move_ids
        insumo = movimiento.product_id
        if insumo.tracking == 'lot':
            movimiento.move_line_ids.unlink()
            for nombre, dias, cant in lotes:
                self.env['stock.move.line'].create({
                    'move_id': movimiento.id,
                    'picking_id': recepcion.id,
                    'product_id': insumo.id,
                    'product_uom_id': movimiento.product_uom.id,
                    'location_id': movimiento.location_id.id,
                    'location_dest_id': movimiento.location_dest_id.id,
                    'quantity': cant,
                    'lot_name': nombre,
                    'expiration_date': fields.Datetime.now() + timedelta(days=dias),
                })
        else:
            movimiento.move_line_ids.quantity = cantidad or movimiento.product_uom_qty
        movimiento.picked = True
        contexto = {'skip_expired': True, 'skip_backorder': True}
        if not con_pendiente:
            contexto['picking_ids_not_to_backorder'] = recepcion.ids
        recepcion.with_context(**contexto).button_validate()
        return recepcion

    def _comprar(self, insumo, cantidad, lotes=None):
        """OC directa → confirmar → recibir toda la cantidad. Sin ``lotes``, un solo lote que vence en 100 días."""
        orden = self._oc(insumo, cantidad)
        orden.button_confirm()
        self._recibir_oc(orden, lotes or [(f'{insumo.default_code}-OC', 100, cantidad)])
        return orden

    def _abastecer_receta(self, excepto=None):
        """Compra y recibe todo lo que pide la OP de ``cantidad_op`` (menos ``excepto``); devuelve {insumo: OC}."""
        ordenes = {}
        for linea in self.bom.bom_line_ids:
            insumo = linea.product_id
            if insumo == excepto:
                continue
            ordenes[insumo] = self._comprar(insumo, linea.product_qty * self.cantidad_op / self.bom.product_qty)
        return ordenes

    def _orden_produccion(self):
        orden = self.env['mrp.production'].create({
            'product_id': self.helado.id,
            'product_qty': self.cantidad_op,
            'bom_id': self.bom.id,
        })
        orden.action_confirm()
        orden.action_assign()
        return orden

    def _producir(self, orden):
        """Produce todo con 1 h de trabajo por operación y cierra la OP."""
        orden.action_generate_serial()
        orden.qty_producing = orden.product_qty
        orden.move_raw_ids.picked = True
        ahora = fields.Datetime.now()
        for operacion in orden.workorder_ids:
            operacion.write({'time_ids': [Command.create({
                'workcenter_id': operacion.workcenter_id.id,
                'loss_id': self.env.ref('mrp.block_reason7').id,
                'date_start': ahora - timedelta(hours=1),
                'date_end': ahora,
            })], 'state': 'done'})
        orden.with_context(skip_backorder=True).button_mark_done()
        return orden

    def _planificar_leche(self):
        """Mismos pasos que la tarea programada del planificador, solo para la regla de la leche."""
        regla = self.env['stock.warehouse.orderpoint'].browse(self.regla_leche.id)
        regla.sudo()._compute_qty_to_order_computed()
        regla.sudo()._procure_orderpoint_confirm(company_id=self.env.company)

    def _rfq_leche(self):
        return self.env['purchase.order.line'].search([
            ('product_id', '=', self.leche.id), ('order_id.state', '=', 'draft')]).order_id

    def _lote_de(self, insumo, nombre):
        return self.Lote.search([('name', '=', nombre), ('product_id', '=', insumo.id)])

    def _consumido_por_lote(self, orden, insumo):
        """{lote: cantidad} de lo que la OP reservó (o consumió) de un insumo."""
        movimiento = orden.move_raw_ids.filtered(lambda m: m.product_id == insumo)
        consumo = {}
        for linea in movimiento.move_line_ids:
            consumo[linea.lot_id] = consumo.get(linea.lot_id, 0) + linea.quantity
        return consumo

    # --- Flujo completo --------------------------------------------------------------------------------

    def test_flujo_completo_del_planificador_al_lote_terminado(self):
        # 1. La leche está en cero: el planificador arma la RFQ hasta el máximo y el comprador la confirma
        self._planificar_leche()
        orden_leche = self._rfq_leche()
        self.assertEqual(orden_leche.order_line.product_qty, self.regla_leche.product_max_qty)
        orden_leche.button_confirm()
        self.assertEqual(orden_leche.state, 'purchase')
        self.assertEqual(orden_leche.receipt_status, 'pending')

        # 2. Llega en dos lotes; el que vence antes entra después, para que FEFO no coincida con el orden de llegada
        maximo = int(self.regla_leche.product_max_qty)
        recepcion = self._recibir_oc(orden_leche, [
            ('LECHE-FLUJO-TARDE', 9, maximo - 3000),
            ('LECHE-FLUJO-PRONTO', 5, 3000),
        ])
        lote_tarde = self._lote_de(self.leche, 'LECHE-FLUJO-TARDE')
        lote_pronto = self._lote_de(self.leche, 'LECHE-FLUJO-PRONTO')
        self.assertEqual(recepcion.state, 'done')
        self.assertEqual(orden_leche.receipt_status, 'full')
        self.assertEqual(orden_leche.order_line.qty_received, maximo)
        self.assertAlmostEqual(
            lote_pronto.expiration_date, fields.Datetime.now() + timedelta(days=5), delta=timedelta(minutes=5))
        self.assertEqual(self._disponible(self.leche, lote_pronto), 3000)
        self.assertEqual(self._disponible(self.leche, lote_tarde), maximo - 3000)

        # 3. Recepción valorada al precio de la OC y con su asiento
        precio_leche = orden_leche.order_line.price_unit
        movimiento_leche = recepcion.move_ids
        self.assertAlmostEqual(movimiento_leche.value, maximo * precio_leche, places=2)
        asiento_leche = movimiento_leche.account_move_id
        self.assertEqual(asiento_leche.state, 'posted')
        self.assertAlmostEqual(asiento_leche.amount_total, maximo * precio_leche, places=2)
        cuenta_existencias = self.leche.categ_id.property_stock_valuation_account_id
        self.assertAlmostEqual(
            sum(asiento_leche.line_ids.filtered(lambda a: a.account_id == cuenta_existencias).mapped('debit')),
            maximo * precio_leche, places=2, msg='La compra debe cargar la cuenta de existencias de los lácteos')

        # 4. Los demás insumos se compran por OC directa, cada uno a su proveedor y a su precio de la ficha
        ordenes = self._abastecer_receta(excepto=self.leche)
        self.assertEqual(len(ordenes), 5)
        for insumo, orden in ordenes.items():
            with self.subTest(insumo=insumo.default_code):
                self.assertEqual(orden.state, 'purchase')
                self.assertEqual(orden.partner_id, insumo.seller_ids[0].partner_id)
                self.assertEqual(orden.receipt_status, 'full')

        # 5. La OP reserva todo y la leche sale del lote que vence antes (el último en llegar)
        orden = self._orden_produccion()
        self.assertEqual(orden.state, 'confirmed')
        self.assertEqual(set(orden.move_raw_ids.mapped('state')), {'assigned'})
        self.assertEqual(self._consumido_por_lote(orden, self.leche), {lote_pronto: 10})

        # 6. Producir: lote del terminado con vencimiento a 12 meses, alerta y retiro según la ficha
        self._producir(orden)
        self.assertEqual(orden.state, 'done')
        self.assertEqual(orden.qty_produced, self.cantidad_op)
        lote_helado = orden.lot_producing_ids
        self.assertEqual(len(lote_helado), 1)
        self.assertAlmostEqual(
            lote_helado.expiration_date,
            fields.Datetime.now() + timedelta(days=self.plantilla.expiration_time),
            delta=timedelta(minutes=5))
        self.assertEqual((lote_helado.expiration_date - lote_helado.alert_date).days, self.plantilla.alert_time)
        self.assertEqual((lote_helado.expiration_date - lote_helado.removal_date).days, self.plantilla.removal_time)
        self.assertEqual(self._disponible(self.helado, lote_helado, orden.location_dest_id), self.cantidad_op)

        # 7. Existencias: los insumos bajan lo que pide la receta; el resto de la leche sigue en su lote
        self.assertEqual(self._disponible(self.leche, lote_pronto), 3000 - 10)
        self.assertEqual(self._disponible(self.leche, lote_tarde), maximo - 3000)
        for insumo, orden_compra in ordenes.items():
            comprado = orden_compra.order_line.product_qty
            self.assertEqual(self.Quant._get_available_quantity(insumo, self.lim.lot_stock_id), 0, insumo.name)
            self.assertEqual(comprado, orden.move_raw_ids.filtered(lambda m: m.product_id == insumo).quantity)

        # 8. Costo: insumos al precio pagado al proveedor + horas de cada centro de trabajo
        precios = {insumo: oc.order_line.price_unit for insumo, oc in ordenes.items()}
        precios[self.leche] = precio_leche
        costo_insumos = sum(
            m.quantity * precios[m.product_id] for m in orden.move_raw_ids)
        self.assertAlmostEqual(costo_insumos, 110.4, places=2, msg='4 kg pulpa, 3 kg azúcar, 1 kg glucosa, 10 L leche, 100 palitos y 100 envolturas')
        self.assertAlmostEqual(sum(m.value for m in orden.move_raw_ids), costo_insumos, places=2)
        costo_horas = sum(wo.workcenter_id.costs_hour for wo in orden.workorder_ids)   # 4 operaciones × 1 h
        terminado = orden.move_finished_ids.filtered(lambda m: m.product_id == self.helado)
        self.assertAlmostEqual(terminado.value, costo_insumos + costo_horas, delta=0.05)
        self.assertAlmostEqual(terminado.price_unit, (costo_insumos + costo_horas) / self.cantidad_op, delta=0.001)

        # 9. Asientos: el de lo terminado queda publicado por el mismo valor y cada insumo consumido tiene el suyo
        self.assertEqual(terminado.account_move_id.state, 'posted')
        self.assertAlmostEqual(terminado.account_move_id.amount_total, terminado.value, places=2)
        for consumo in orden.move_raw_ids:
            with self.subTest(consumo=consumo.product_id.default_code):
                self.assertEqual(consumo.account_move_id.state, 'posted')

        # 10. La leche sigue sobre el mínimo: el planificador no vuelve a pedir
        self._planificar_leche()
        self.assertFalse(self._rfq_leche())

    # --- Recepción parcial -----------------------------------------------------------------------------

    def test_recepcion_parcial_deja_la_oc_abierta_hasta_completar(self):
        orden = self._oc(self.leche, 100)
        orden.button_confirm()
        precio = orden.order_line.price_unit

        primera = self._recibir_oc(orden, [('LECHE-PARCIAL-1', 4, 60)], con_pendiente=True)

        self.assertEqual(primera.state, 'done')
        self.assertEqual(orden.state, 'purchase', 'La OC sigue abierta mientras falte mercadería')
        self.assertEqual(orden.receipt_status, 'partial')
        self.assertEqual(orden.order_line.qty_received, 60)
        pendiente = orden.picking_ids - primera
        self.assertEqual(len(pendiente), 1)
        self.assertEqual(pendiente.backorder_id, primera)
        self.assertEqual(pendiente.state, 'assigned')
        self.assertEqual(pendiente.move_ids.product_uom_qty, 40)
        self.assertAlmostEqual(primera.move_ids.value, 60 * precio, places=2)
        self.assertEqual(self._disponible(self.leche, self._lote_de(self.leche, 'LECHE-PARCIAL-1')), 60)

        segunda = self._recibir_oc(orden, [('LECHE-PARCIAL-2', 8, 40)])

        self.assertEqual(segunda.state, 'done')
        self.assertEqual(orden.receipt_status, 'full')
        self.assertEqual(orden.order_line.qty_received, 100)
        self.assertAlmostEqual(segunda.move_ids.value, 40 * precio, places=2)
        lote_1 = self._lote_de(self.leche, 'LECHE-PARCIAL-1')
        lote_2 = self._lote_de(self.leche, 'LECHE-PARCIAL-2')
        self.assertLess(lote_1.expiration_date, lote_2.expiration_date, 'Cada entrega conserva su propio vencimiento')
        self.assertEqual(self._disponible(self.leche, lote_2), 40)
        self.assertAlmostEqual(self.leche.total_value, 100 * precio, places=2)

    # --- La OP consume por vencimiento, no por orden de llegada -----------------------------------------

    def test_la_op_agota_el_lote_que_vence_antes_aunque_llego_despues(self):
        self._abastecer_receta(excepto=self.leche)
        self._comprar(self.leche, 20, [('LECHE-LLEGO-PRIMERO', 9, 20)])
        self._comprar(self.leche, 6, [('LECHE-LLEGO-DESPUES', 4, 6)])
        primero = self._lote_de(self.leche, 'LECHE-LLEGO-PRIMERO')
        despues = self._lote_de(self.leche, 'LECHE-LLEGO-DESPUES')

        orden = self._orden_produccion()

        # La receta pide 10 L: salen los 6 L que vencen antes y 4 L del otro lote
        self.assertEqual(self._consumido_por_lote(orden, self.leche), {despues: 6, primero: 4})
        self._producir(orden)
        self.assertEqual(orden.state, 'done')
        self.assertEqual(self._disponible(self.leche, despues), 0)
        self.assertEqual(self._disponible(self.leche, primero), 16)
        consumido = orden.move_raw_ids.filtered(lambda m: m.product_id == self.leche)
        self.assertEqual(
            {ml.lot_id: ml.quantity for ml in consumido.move_line_ids}, {despues: 6, primero: 4},
            'Lo consumido queda trazado por lote')

    # --- La OP espera la mercadería y se completa al recibir la compra ----------------------------------

    def test_la_op_espera_el_insumo_y_se_completa_al_recibir_la_compra(self):
        self._abastecer_receta(excepto=self.leche)
        orden = self._orden_produccion()
        leche = orden.move_raw_ids.filtered(lambda m: m.product_id == self.leche)
        self.assertEqual(orden.reservation_state, 'confirmed', 'Falta leche: la OP no puede estar lista')
        self.assertEqual(leche.state, 'confirmed')
        self.assertFalse(leche.move_line_ids)

        compra = self._comprar(self.leche, 10, [('LECHE-LLEGA-TARDE', 5, 10)])
        orden.action_assign()

        self.assertEqual(compra.receipt_status, 'full')
        self.assertEqual(orden.reservation_state, 'assigned')
        lote = self._lote_de(self.leche, 'LECHE-LLEGA-TARDE')
        self.assertEqual(self._consumido_por_lote(orden, self.leche), {lote: 10})
        self._producir(orden)
        self.assertEqual(orden.state, 'done')
        self.assertEqual(self._disponible(self.leche, lote), 0)
        self.assertEqual(self._disponible(self.helado, orden.lot_producing_ids, orden.location_dest_id), self.cantidad_op)
