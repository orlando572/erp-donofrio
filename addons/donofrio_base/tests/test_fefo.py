from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestLotesYFefo(DonofrioStockCase):
    """HU-11 (RF006, RNF005): lotes con vencimiento, salida FEFO y alerta 30 días antes."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.helado = cls._producto('pt_h01')
        cls.leche = cls._producto('in_leche')
        cls.tipo_pick = cls.lim.pick_type_id
        cls.salida = cls.lim.wh_output_stock_loc_id

    def _reservar(self, producto, cantidad):
        picking = self._picking(self.tipo_pick, self.lim.lot_stock_id, self.salida, producto, cantidad)
        picking.action_assign()
        return picking

    # --- Recepción: se pide el lote y la fecha ---------------------------------------------------------

    def test_recepcion_sin_lote_no_se_valida(self):
        picking = self._recibir(self.helado, 10)
        with self.assertRaises(UserError):
            picking.button_validate()

    def test_recepcion_con_lote_guarda_la_fecha_de_vencimiento(self):
        picking = self._recibir(self.helado, 10, lote='H01-REC-001', dias_para_vencer=200)
        picking.with_context(skip_expired=True).button_validate()
        self.assertEqual(picking.state, 'done')
        lote = self.Lote.search([('name', '=', 'H01-REC-001'), ('product_id', '=', self.helado.id)])
        self.assertEqual(len(lote), 1)
        dias = (lote.expiration_date - fields.Datetime.now()).days
        self.assertIn(dias, (199, 200))
        self.assertEqual(self._disponible(self.helado, lote), 10)

    def test_recepcion_sin_fecha_usa_la_vida_util_del_producto(self):
        """Si no se escribe la fecha, el lote vence según la vida útil (leche: 10 días)."""
        picking = self._recibir(self.leche, 50, lote='LECHE-REC-001')
        picking.with_context(skip_expired=True).button_validate()
        lote = self.Lote.search([('name', '=', 'LECHE-REC-001'), ('product_id', '=', self.leche.id)])
        self.assertIn((lote.expiration_date - fields.Datetime.now()).days, (9, 10))

    # --- Salida FEFO ----------------------------------------------------------------------------------

    def test_la_entrega_reserva_primero_el_lote_que_vence_antes(self):
        # Se ingresan en orden inverso al de vencimiento para que no coincida con el orden FIFO
        lejano = self._lote(self.helado, 'H01-LEJANO', 300)
        medio = self._lote(self.helado, 'H01-MEDIO', 200)
        proximo = self._lote(self.helado, 'H01-PROXIMO', 100)
        for lote in (lejano, medio, proximo):
            self._stock(self.helado, lote, 10)

        picking = self._reservar(self.helado, 12)

        self.assertEqual(picking.state, 'assigned')
        reservado = {ml.lot_id: ml.quantity for ml in picking.move_ids.move_line_ids}
        self.assertEqual(reservado, {proximo: 10, medio: 2})

    def test_fefo_ordena_por_vencimiento_y_no_por_antiguedad_del_ingreso(self):
        viejo_ingreso = self._lote(self.helado, 'H01-INGRESO-1', 365)
        self._stock(self.helado, viejo_ingreso, 5)
        nuevo_ingreso = self._lote(self.helado, 'H01-INGRESO-2', 90)
        self._stock(self.helado, nuevo_ingreso, 5)

        picking = self._reservar(self.helado, 5)

        self.assertEqual(picking.move_ids.move_line_ids.lot_id, nuevo_ingreso)

    def test_pick_y_ship_en_lima_respetan_el_lote_reservado(self):
        """El segundo paso (ship) toma el mismo lote que el pick, sin volver a elegir."""
        otro = self._lote(self.helado, 'H01-OTRO', 250)
        proximo = self._lote(self.helado, 'H01-VENCE-ANTES', 60)
        self._stock(self.helado, otro, 4)
        self._stock(self.helado, proximo, 4)
        pick = self._reservar(self.helado, 3)
        pick.move_ids.picked = True
        pick.button_validate()
        self.assertEqual(pick.state, 'done')

        ship = pick.move_ids.move_dest_ids.picking_id
        ship.action_assign()
        self.assertEqual(ship.picking_type_id, self.lim.out_type_id)
        self.assertEqual(ship.move_ids.move_line_ids.lot_id, proximo)

    # --- RNF005: no se despacha un lote vencido -------------------------------------------------------

    def test_lote_vencido_no_se_reserva(self):
        vencido = self._lote(self.helado, 'H01-VENCIDO', -5)
        vigente = self._lote(self.helado, 'H01-VIGENTE', 150)
        self._stock(self.helado, vencido, 10)
        self._stock(self.helado, vigente, 4)
        quant_vencido = self.Quant.search([('lot_id', '=', vencido.id)])
        self.assertEqual(quant_vencido.quantity, 10)
        self.assertEqual(quant_vencido.available_quantity, 0)

        picking = self._reservar(self.helado, 8)

        lotes = picking.move_ids.move_line_ids.lot_id
        self.assertNotIn(vencido, lotes)
        self.assertEqual(sum(picking.move_ids.move_line_ids.mapped('quantity')), 4)
        self.assertEqual(picking.move_ids.state, 'partially_available')

    def test_lote_en_fecha_de_retiro_no_se_reserva(self):
        """Un lote que aún no venció pero ya pasó su fecha de retiro tampoco sale (leche: retiro 1 día antes)."""
        por_retirar = self._lote(self.leche, 'LECHE-RETIRO', 0)
        vigente = self._lote(self.leche, 'LECHE-VIGENTE', 8)
        self._stock(self.leche, por_retirar, 20)
        self._stock(self.leche, vigente, 20)

        picking = self._reservar(self.leche, 10)

        self.assertEqual(picking.move_ids.move_line_ids.lot_id, vigente)

    # --- Alerta 30 días antes -------------------------------------------------------------------------

    def test_alerta_a_30_dias_del_vencimiento(self):
        por_vencer = self._lote(self.helado, 'H01-POR-VENCER', 25)
        lejano = self._lote(self.helado, 'H01-SIN-ALERTA', 100)
        self.assertEqual(
            (por_vencer.expiration_date - por_vencer.alert_date).days, 30,
            'La alerta debe saltar 30 días antes del vencimiento')
        self._stock(self.helado, por_vencer, 5)
        self._stock(self.helado, lejano, 5)

        self.Lote._alert_date_exceeded()

        self.assertTrue(por_vencer.product_expiry_reminded)
        self.assertFalse(lejano.product_expiry_reminded)
        actividad = por_vencer.activity_ids
        self.assertEqual(len(actividad), 1)
        self.assertFalse(lejano.activity_ids)

    def test_alerta_llega_al_jefe_de_almacen(self):
        por_vencer = self._lote(self.helado, 'H01-ALERTA-JEFE', 10)
        self._stock(self.helado, por_vencer, 5)

        self.Lote._alert_date_exceeded()

        self.assertEqual(por_vencer.activity_ids.user_id, self.env.ref('donofrio_base.user_jefe_almacen'))
