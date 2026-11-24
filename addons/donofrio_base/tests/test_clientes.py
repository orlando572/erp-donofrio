from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestClientes(TransactionCase):
    """HU-16: 30 clientes ficticios por canal, cada uno con su lista de precios y su plazo de pago."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.clientes = cls.env['res.partner'].search([('id', 'in', cls.env['ir.model.data'].search([
            ('module', '=', 'donofrio_base'), ('model', '=', 'res.partner'), ('name', '=like', 'cli_%')]).mapped('res_id'))])

    def test_treinta_clientes_con_documento_valido(self):
        self.assertEqual(len(self.clientes), 30)
        for cliente in self.clientes:
            with self.subTest(cliente=cliente.name):
                tipo = cliente.l10n_latam_identification_type_id
                self.assertIn(tipo, self.env.ref('l10n_pe.it_RUC') | self.env.ref('l10n_pe.it_DNI'))
                self.assertEqual(len(cliente.vat), 11 if tipo == self.env.ref('l10n_pe.it_RUC') else 8)
        self.assertEqual(len(set(self.clientes.mapped('vat'))), 30, 'Los documentos no se repiten')

    def test_cada_canal_con_su_lista(self):
        esperado = {
            'cat_distribuidor': ('lista_mayorista', 6),
            'cat_autoservicio': ('lista_mayorista', 6),
            'cat_bodega': ('lista_bodega', 10),
            'cat_heladero': ('lista_heladero', 8),
        }
        for categoria, (lista, cantidad) in esperado.items():
            with self.subTest(canal=categoria):
                grupo = self.clientes.filtered(lambda c: self.env.ref(f'donofrio_base.{categoria}') in c.category_id)
                self.assertEqual(len(grupo), cantidad)
                self.assertEqual(grupo.property_product_pricelist, self.env.ref(f'donofrio_base.{lista}'))

    def test_los_heladeros_y_bodegueros_con_dni_reciben_boleta(self):
        heladeros = self.clientes.filtered(lambda c: self.env.ref('donofrio_base.cat_heladero') in c.category_id)
        self.assertTrue(all(c.l10n_latam_identification_type_id == self.env.ref('l10n_pe.it_DNI') for c in heladeros))
