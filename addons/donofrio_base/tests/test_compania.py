from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestCompania(TransactionCase):
    """HU-03: la compañía queda con la localización peruana, cargada por código."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.compania = cls.env.ref('base.main_company')

    def test_identidad_fiscal(self):
        self.assertTrue(self.compania.name.startswith("D'Onofrio"))
        self.assertEqual(self.compania.country_id.code, 'PE')
        self.assertEqual(self.compania.vat, '20999999990')
        self.assertEqual(
            self.compania.partner_id.l10n_latam_identification_type_id,
            self.env.ref('l10n_pe.it_RUC'),
        )

    def test_ruc_valido(self):
        """El RUC ficticio pasa la validación de dígito verificador de stdnum."""
        from stdnum.pe import ruc
        self.assertTrue(ruc.is_valid(self.compania.vat))

    def test_moneda_pen(self):
        self.assertEqual(self.compania.currency_id.name, 'PEN')
        self.assertTrue(self.compania.currency_id.active)

    def test_plan_contable_peruano(self):
        self.assertEqual(self.compania.chart_template, 'pe')
        self.assertEqual(self.compania.account_fiscal_country_id.code, 'PE')

    def test_igv_18(self):
        impuesto_venta = self.compania.account_sale_tax_id
        self.assertEqual(impuesto_venta.amount, 18.0)
        self.assertEqual(impuesto_venta.amount_type, 'percent')
        self.assertEqual(impuesto_venta.type_tax_use, 'sale')
        impuesto_compra = self.compania.account_purchase_tax_id
        self.assertEqual(impuesto_compra.amount, 18.0)
        self.assertEqual(impuesto_compra.type_tax_use, 'purchase')

    def test_idioma_y_zona_horaria(self):
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', 'es_PE')])
        self.assertTrue(lang.active)
        self.assertEqual(self.compania.partner_id.lang, 'es_PE')
        self.assertEqual(self.compania.partner_id.tz, 'America/Lima')
        admin = self.env.ref('base.user_admin')
        self.assertEqual(admin.lang, 'es_PE')
        self.assertEqual(admin.tz, 'America/Lima')

    def test_identidad_visual(self):
        self.assertTrue(self.compania.logo)
        self.assertEqual(self.compania.primary_color, '#C77D00')
        self.assertEqual(self.compania.secondary_color, '#5B3A29')
        self.assertEqual(self.compania.external_report_layout_id, self.env.ref('web.external_layout_standard'))
