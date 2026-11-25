from odoo import fields
from odoo.tests import tagged

from .common import CasoLoteRechazado


@tagged('post_install', '-at_install')
class TestBloqueoEnPuntoDeVenta(CasoLoteRechazado):
    """HU-17: el despacho de un lote rechazado también se frena cuando sale por el PdV (RNF005)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = cls.env.ref('donofrio_base.pos_config_venezuela')
        cls.efectivo = cls.env.ref('donofrio_base.pdv_metodo_efectivo')
        cls.origen = cls.config.picking_type_id.default_location_src_id
        cls.rechazado = cls._lote(cls.helado, 'LOTE-RECH-PDV', 200)
        cls.aprobado = cls._lote(cls.helado, 'LOTE-OK-PDV', 200)
        for lote in (cls.rechazado, cls.aprobado):
            cls._stock(cls.helado, lote, 10, cls.origen)
        cls._inspeccion_de(cls.rechazado, 'rechazada')

    def _vender(self, sesion, lote, cantidad=2):
        """Venta como la envía la interfaz del PdV, con el lote tecleado por el cajero."""
        precio = self.config.pricelist_id._get_product_price(self.helado, cantidad)
        impuestos = self.helado.taxes_id.filtered_domain(self.env['account.tax']._check_company_domain(self.env.company))
        calculo = impuestos.compute_all(precio, sesion.currency_id, cantidad)
        total = calculo['total_included']
        uuid = f'00000-000-{self.env["pos.order"].search_count([]):04d}'
        datos = {
            'amount_paid': total, 'amount_return': 0, 'amount_tax': total - calculo['total_excluded'],
            'amount_total': total, 'date_order': fields.Datetime.to_string(fields.Datetime.now()),
            'pricelist_id': self.config.pricelist_id.id, 'name': f'Order {uuid}', 'uuid': uuid,
            'last_order_preparation_change': '{}', 'session_id': sesion.id, 'user_id': self.env.uid,
            'partner_id': False, 'to_invoice': False, 'fiscal_position_id': False,
            'lines': [(0, 0, {
                'id': 1, 'pack_lot_ids': [[0, 0, {'lot_name': lote.name}]], 'price_unit': precio,
                'product_id': self.helado.id, 'qty': cantidad,
                'price_subtotal': calculo['total_excluded'], 'price_subtotal_incl': total,
                'tax_ids': [(6, 0, impuestos.ids)],
            })],
            'payment_ids': [(0, 0, {'amount': total, 'name': fields.Datetime.now(), 'payment_method_id': self.efectivo.id})],
        }
        resultado = self.env['pos.order'].sync_from_ui([datos])
        return self.env['pos.order'].browse(resultado['pos.order'][0]['id'])

    def _en_mano(self, lote):
        """Existencia física del lote en el almacén del PdV (no resta lo reservado por una salida pendiente)."""
        return sum(self.Quant._gather(self.helado, self.origen, lot_id=lote).mapped('quantity'))

    def _sesion(self):
        self.config.open_ui()
        sesion = self.config.current_session_id
        sesion.set_opening_control(0.0, None)
        return sesion

    def test_el_pdv_no_saca_del_stock_un_lote_rechazado(self):
        """El PdV traga el UserError (try/except en _create_picking_from_pos_order_lines): la venta se registra,
        pero la salida de stock del lote rechazado no se valida: queda reservada y el lote sigue en el almacén."""
        pedido = self._vender(self._sesion(), self.rechazado)
        picking = pedido.picking_ids
        self.assertTrue(picking)
        self.assertNotEqual(picking.state, 'done')
        self.assertEqual(self._en_mano(self.rechazado), 10)
        cliente = self.env.ref('stock.stock_location_customers')
        self.assertEqual(self.Quant._get_available_quantity(self.helado, cliente, lot_id=self.rechazado, strict=True), 0)

    def test_el_pdv_despacha_un_lote_aprobado(self):
        pedido = self._vender(self._sesion(), self.aprobado)
        self.assertEqual(pedido.picking_ids.state, 'done')
        self.assertEqual(self._en_mano(self.aprobado), 8)
