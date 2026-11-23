from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestListasDePrecios(TransactionCase):
    """HU-09: el precio cambia según la lista y la fecha, y el pedido confirmado genera la entrega."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ref = cls.env.ref
        cls.helado = ref('donofrio_base.pt_h01').product_variant_id      # 1.50
        cls.paneton = cls.env['product.product'].search([('default_code', '=', 'PT-P01')])
        cls.verano = ref('donofrio_base.lista_verano')
        cls.navidad = ref('donofrio_base.lista_navidad')

    def _precio(self, lista, producto, fecha):
        return lista._get_product_price(producto, 1.0, date=fields.Datetime.to_datetime(fecha))

    def test_cinco_listas_en_soles(self):
        for xmlid in ('mayorista', 'bodega', 'heladero', 'verano', 'navidad'):
            with self.subTest(lista=xmlid):
                lista = self.env.ref(f'donofrio_base.lista_{xmlid}')
                self.assertEqual(lista.currency_id.name, 'PEN')
                self.assertTrue(lista.item_ids)

    def test_listas_por_canal(self):
        base = self.helado.lst_price
        esperado = {'mayorista': 0.85, 'bodega': 0.92, 'heladero': 0.75}
        for xmlid, factor in esperado.items():
            with self.subTest(lista=xmlid):
                lista = self.env.ref(f'donofrio_base.lista_{xmlid}')
                self.assertAlmostEqual(self._precio(lista, self.helado, '2026-06-15'), base * factor)

    def test_verano_depende_de_la_fecha_y_la_categoria(self):
        base = self.helado.lst_price
        self.assertAlmostEqual(self._precio(self.verano, self.helado, '2027-01-15'), base * 0.90)
        self.assertAlmostEqual(self._precio(self.verano, self.helado, '2026-07-15'), base)
        # el panetón no entra en la lista de verano
        self.assertAlmostEqual(self._precio(self.verano, self.paneton, '2027-01-15'), self.paneton.lst_price)

    def test_navidad_depende_de_la_fecha_y_la_categoria(self):
        base = self.paneton.lst_price
        self.assertAlmostEqual(self._precio(self.navidad, self.paneton, '2026-11-20'), base * 0.88)
        self.assertAlmostEqual(self._precio(self.navidad, self.paneton, '2026-05-20'), base)
        self.assertAlmostEqual(self._precio(self.navidad, self.helado, '2026-11-20'), self.helado.lst_price)

    def test_pedido_confirmado_genera_entrega_con_precio_de_la_lista(self):
        cliente = self.env['res.partner'].create({'name': 'Bodega de prueba'})
        pedido = self.env['sale.order'].create({
            'partner_id': cliente.id,
            'pricelist_id': self.env.ref('donofrio_base.lista_heladero').id,
            'order_line': [(0, 0, {'product_id': self.helado.id, 'product_uom_qty': 10})],
        })
        self.assertAlmostEqual(pedido.order_line.price_unit, self.helado.lst_price * 0.75)
        pedido.action_confirm()
        self.assertEqual(pedido.state, 'sale')
        self.assertTrue(pedido.picking_ids, 'El pedido confirmado debe generar la entrega')
