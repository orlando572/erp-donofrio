from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestPuntoDeVenta(TransactionCase):
    """HU-10: sesión de PdV, venta, boleta con DNI o consumidor final y cierre de caja cuadrado."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = cls.env.ref('donofrio_base.pos_config_venezuela')
        cls.cajero = cls.env.ref('donofrio_base.user_cajero_pdv')
        cls.efectivo = cls.env.ref('donofrio_base.pdv_metodo_efectivo')
        cls.yape = cls.env.ref('donofrio_base.pdv_metodo_yape')
        cls.helado = cls.env.ref('donofrio_base.pt_h01').product_variant_id
        cls.consumidor_final = cls.env.ref('l10n_pe_pos.partner_pe_cf')
        cls.cliente_dni = cls.env['res.partner'].create({
            'name': 'Cliente con DNI de prueba',
            'l10n_latam_identification_type_id': cls.env.ref('l10n_pe.it_DNI').id,
            'vat': '12345678',
        })

    def _abrir_sesion(self, efectivo_inicial=0.0, usuario=None):
        config = self.config.with_user(usuario) if usuario else self.config
        config.open_ui()
        sesion = config.current_session_id
        sesion.set_opening_control(efectivo_inicial, None)
        return sesion

    def _vender(self, sesion, cantidad, metodo, cliente=False, boleta=False, usuario=None, lote=None):
        """Registra una venta como lo hace la interfaz del PdV y devuelve el pedido."""
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
            'partner_id': cliente.id if cliente else False, 'to_invoice': boleta,
            'fiscal_position_id': False,
            'lines': [(0, 0, {
                'id': 1, 'pack_lot_ids': [[0, 0, {'lot_name': lote}]] if lote else [], 'price_unit': precio, 'product_id': self.helado.id, 'qty': cantidad,
                'price_subtotal': calculo['total_excluded'], 'price_subtotal_incl': total,
                'tax_ids': [(6, 0, impuestos.ids)],
            })],
            'payment_ids': [(0, 0, {
                'amount': total, 'name': fields.Datetime.now(), 'payment_method_id': metodo.id,
            })],
        }
        pedidos = self.env['pos.order'].with_user(usuario) if usuario else self.env['pos.order']
        resultado = pedidos.sync_from_ui([datos])
        return self.env['pos.order'].browse(resultado['pos.order'][0]['id']), total

    def test_pdv_con_efectivo_y_yape(self):
        self.assertEqual(self.config.name, 'Heladería Av. Venezuela')
        self.assertEqual(self.config.payment_method_ids, self.efectivo | self.yape)
        self.assertTrue(self.efectivo.is_cash_count)
        self.assertFalse(self.yape.is_cash_count)
        self.assertEqual(self.config.picking_type_id.warehouse_id, self.env.ref('stock.warehouse0'))

    def test_catalogo_del_pdv_son_los_productos_terminados(self):
        terminados = self.env['product.template'].search([
            ('categ_id', 'child_of', self.env.ref('donofrio_base.cat_terminados').id)])
        insumos = self.env['product.template'].search([
            ('categ_id', 'child_of', self.env.ref('donofrio_base.cat_insumos').id)])
        self.assertTrue(terminados)
        self.assertTrue(all(terminados.mapped('available_in_pos')), 'El cajero debe poder vender todo producto terminado')
        self.assertFalse(any(insumos.mapped('available_in_pos')), 'Los insumos no se venden en el PdV')

    def test_boleta_a_consumidor_final(self):
        sesion = self._abrir_sesion()
        pedido, total = self._vender(sesion, 4, self.efectivo, self.consumidor_final, boleta=True)
        self.assertEqual(pedido.state, 'done')
        factura = pedido.account_move
        self.assertTrue(factura, 'La venta con boleta debe generar la factura')
        self.assertEqual(factura.state, 'posted')
        self.assertEqual(factura.l10n_latam_document_type_id.code, '03')   # Boleta de venta electrónica
        self.assertAlmostEqual(factura.amount_total, total)

    def test_boleta_a_cliente_con_dni(self):
        sesion = self._abrir_sesion()
        pedido, _total = self._vender(sesion, 2, self.yape, self.cliente_dni, boleta=True)
        factura = pedido.account_move
        self.assertEqual(factura.partner_id, self.cliente_dni)
        self.assertEqual(factura.l10n_latam_document_type_id.code, '03')

    def test_cierre_de_caja_cuadrado(self):
        sesion = self._abrir_sesion(efectivo_inicial=50.0)
        _pedido, total_efectivo = self._vender(sesion, 4, self.efectivo)
        self._vender(sesion, 2, self.yape)
        contado = 50.0 + total_efectivo   # solo el efectivo entra a la caja; Yape no
        sesion.post_closing_cash_details(contado)
        resultado = sesion.close_session_from_ui()
        self.assertTrue(resultado['successful'], resultado)
        self.assertEqual(sesion.state, 'closed')
        self.assertAlmostEqual(sesion.cash_register_difference, 0.0)

    def test_cajero_vende_con_lote_y_boleta_sin_permisos_de_inventario(self):
        """Los productos terminados llevan lote: el cajero, que no es usuario de Inventario, debe poder venderlos."""
        sesion = self._abrir_sesion(usuario=self.cajero)
        pedido, total = self._vender(
            sesion, 1, self.efectivo, self.consumidor_final, boleta=True, usuario=self.cajero, lote='LOTE-CAJERO-1')
        self.assertEqual(pedido.account_move.l10n_latam_document_type_id.code, '03')
        self.assertEqual(pedido.lines.pack_lot_ids.lot_name, 'LOTE-CAJERO-1')
        sesion = sesion.with_user(self.cajero)
        sesion.post_closing_cash_details(total)
        resultado = sesion.close_session_from_ui()
        self.assertTrue(resultado['successful'], resultado)
        self.assertAlmostEqual(sesion.cash_register_difference, 0.0)
