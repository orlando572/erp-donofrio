from datetime import timedelta

from odoo import Command, fields
from odoo.tests import tagged

from .common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestRecepcionYDespacho(DonofrioStockCase):
    """HU-12 (RF007): recibir insumos desde la OC y despachar en 2 pasos (pick + ship); reposición a AQP."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.leche = cls._producto('in_leche')
        cls.helado = cls._producto('pt_h01')
        cls.proveedor = cls.leche.seller_ids[0].partner_id

    def _orden_de_compra(self, producto, cantidad):
        orden = self.env['purchase.order'].create({
            'partner_id': self.proveedor.id,
            'order_line': [Command.create({
                'product_id': producto.id,
                'product_qty': cantidad,
                'price_unit': producto.standard_price,
            })],
        })
        orden.button_confirm()
        return orden

    # --- Recepción desde la OC ------------------------------------------------------------------------

    def test_oc_confirmada_crea_la_recepcion_en_lima(self):
        orden = self._orden_de_compra(self.leche, 200)
        recepcion = orden.picking_ids
        self.assertEqual(len(recepcion), 1)
        self.assertEqual(recepcion.picking_type_id, self.lim.in_type_id)
        self.assertEqual(recepcion.location_id, self.proveedores)
        self.assertEqual(recepcion.location_dest_id, self.lim.lot_stock_id)
        self.assertEqual(recepcion.move_ids.product_uom_qty, 200)
        self.assertEqual(recepcion.partner_id, self.proveedor)

    def test_recibir_la_oc_con_lote_deja_stock_y_actualiza_lo_recibido(self):
        orden = self._orden_de_compra(self.leche, 200)
        recepcion = orden.picking_ids
        linea = recepcion.move_ids.move_line_ids
        linea.quantity = 200
        linea.lot_name = 'LECHE-OC-001'
        linea.expiration_date = fields.Datetime.now() + timedelta(days=9)
        recepcion.move_ids.picked = True

        recepcion.with_context(skip_expired=True).button_validate()

        self.assertEqual(recepcion.state, 'done')
        self.assertEqual(orden.order_line.qty_received, 200)
        lote = self.Lote.search([('name', '=', 'LECHE-OC-001'), ('product_id', '=', self.leche.id)])
        self.assertEqual(self._disponible(self.leche, lote), 200)

    def test_recepcion_parcial_registra_lo_recibido(self):
        orden = self._orden_de_compra(self.leche, 100)
        recepcion = orden.picking_ids
        linea = recepcion.move_ids.move_line_ids
        linea.quantity = 60
        linea.lot_name = 'LECHE-PARCIAL'
        recepcion.move_ids.picked = True

        # Sin crear entrega pendiente (no backorder): lo recibido queda registrado
        recepcion.with_context(skip_expired=True, skip_backorder=True, picking_ids_not_to_backorder=recepcion.ids).button_validate()
        self.assertEqual(orden.order_line.qty_received, 60)

    # --- Despacho en 2 pasos en Lima -------------------------------------------------------------------

    def test_lima_despacha_en_pick_y_ship(self):
        pick, ship = self.lim.pick_type_id, self.lim.out_type_id
        self.assertTrue(pick.active)
        self.assertEqual(pick.default_location_dest_id, self.lim.wh_output_stock_loc_id)
        self.assertEqual(ship.default_location_src_id, self.lim.wh_output_stock_loc_id)
        self.assertEqual(self.lim.delivery_steps, 'pick_ship')

    def test_el_ship_espera_a_que_termine_el_pick(self):
        lote = self._lote(self.helado, 'H01-2PASOS', 120)
        self._stock(self.helado, lote, 20)
        pick = self._picking(
            self.lim.pick_type_id, self.lim.lot_stock_id, self.lim.wh_output_stock_loc_id, self.helado, 6)
        # El ship lo crea la ruta del almacén cuando la entrega sale de ventas; aquí se arma la cadena a mano
        ship = self._picking(
            self.lim.out_type_id, self.lim.wh_output_stock_loc_id,
            self.env.ref('stock.stock_location_customers'), self.helado, 6)
        pick.move_ids.move_dest_ids = ship.move_ids
        ship.move_ids.write({'procure_method': 'make_to_order'})
        ship.action_assign()
        pick.action_assign()

        self.assertEqual(pick.state, 'assigned')
        self.assertNotEqual(ship.state, 'assigned', 'El ship no puede estar listo antes de terminar el pick')

        pick.move_ids.picked = True
        pick.button_validate()
        self.assertEqual(pick.state, 'done')
        ship.action_assign()
        self.assertEqual(ship.state, 'assigned')
        self.assertEqual(ship.move_ids.move_line_ids.lot_id, lote)

        ship.move_ids.picked = True
        ship.button_validate()
        self.assertEqual(ship.state, 'done')
        self.assertEqual(self._disponible(self.helado, lote), 14)

    # --- Transferencia Lima → Arequipa -----------------------------------------------------------------

    def _reponer_arequipa(self, producto, cantidad):
        regla = self.env['stock.rule']
        regla.run([regla.Procurement(
            producto, cantidad, producto.uom_id, self.aqp.lot_stock_id, 'Reposición AQP', 'TEST-AQP',
            self.env.company, {'warehouse_id': self.aqp, 'route_ids': self.aqp.resupply_route_ids},
        )])
        return self.env['stock.picking'].search([('origin', '=', 'TEST-AQP')], order='id')

    def test_la_reposicion_arma_pick_ship_y_recepcion_en_arequipa(self):
        lote = self._lote(self.helado, 'H01-A-AQP', 180)
        self._stock(self.helado, lote, 30)

        pickings = self._reponer_arequipa(self.helado, 12)

        tipos = pickings.picking_type_id
        self.assertIn(self.lim.pick_type_id, tipos)
        self.assertIn(self.lim.out_type_id, tipos)
        self.assertIn(self.aqp.in_type_id, tipos)
        destino = pickings.move_ids.location_dest_id
        self.assertIn(self.aqp.lot_stock_id, destino)

    def test_la_mercaderia_llega_a_arequipa_con_su_lote(self):
        lote = self._lote(self.helado, 'H01-VIAJE', 180)
        self._stock(self.helado, lote, 30)
        pickings = self._reponer_arequipa(self.helado, 12)

        for _ in range(3):
            pendiente = pickings.filtered(lambda p: p.state == 'assigned')
            self.assertTrue(pendiente, 'Cada paso debe quedar listo cuando termina el anterior')
            pendiente.move_ids.picked = True
            pendiente.button_validate()
            esperando = pickings.filtered(lambda p: p.state in ('confirmed', 'waiting'))
            if esperando:
                esperando.action_assign()

        self.assertEqual(set(pickings.mapped('state')), {'done'})
        self.assertEqual(self._disponible(self.helado, lote, self.aqp.lot_stock_id), 12)
        self.assertEqual(self._disponible(self.helado, lote, self.lim.lot_stock_id), 18)
