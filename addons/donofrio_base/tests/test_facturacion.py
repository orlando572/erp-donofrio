from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestFacturacionConIGV(TransactionCase):
    """HU-15: factura (01) y boleta (03) con IGV desde el pedido, en su diario, con PDF."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.helado = cls.env.ref('donofrio_base.pt_h01').product_variant_id        # S/ 1.50, IGV incluido
        cls.facturas = cls.env.ref('donofrio_base.diario_facturas')
        cls.boletas = cls.env.ref('donofrio_base.diario_boletas')
        cls.cliente_ruc = cls.env['res.partner'].create({
            'name': 'Distribuidora de prueba SAC', 'is_company': True,
            'l10n_latam_identification_type_id': cls.env.ref('l10n_pe.it_RUC').id,
            'vat': '20123456786',
        })
        cls.cliente_dni = cls.env['res.partner'].create({
            'name': 'Cliente con DNI de prueba',
            'l10n_latam_identification_type_id': cls.env.ref('l10n_pe.it_DNI').id,
            'vat': '12345678',
        })

    def _facturar(self, cliente, cantidad=100):
        pedido = self.env['sale.order'].create({
            'partner_id': cliente.id,
            'order_line': [(0, 0, {'product_id': self.helado.id, 'product_uom_qty': cantidad})],
        })
        pedido.action_confirm()
        factura = pedido._create_invoices()
        factura.action_post()
        return pedido, factura

    def test_diarios_de_factura_y_boleta(self):
        for diario in (self.facturas, self.boletas):
            with self.subTest(diario=diario.code):
                self.assertEqual(diario.type, 'sale')
                self.assertTrue(diario.l10n_latam_use_documents)
        # el nombre debe verse igual en la interfaz en español (Odoo traduce «Sales» como «Ventas»)
        for idioma in self.env['res.lang'].search([]).mapped('code'):
            with self.subTest(idioma=idioma):
                self.assertEqual(self.facturas.with_context(lang=idioma).name, 'Facturas')
                self.assertEqual(self.boletas.with_context(lang=idioma).name, 'Boletas')
        self.assertEqual(self.env.ref('donofrio_base.pos_config_venezuela').invoice_journal_id, self.boletas)

    def test_los_terminados_llevan_igv_18_incluido_en_el_precio(self):
        terminados = self.env['product.template'].search([
            ('categ_id', 'child_of', self.env.ref('donofrio_base.cat_terminados').id)])
        for producto in terminados:
            with self.subTest(producto=producto.default_code):
                self.assertEqual(producto.taxes_id.mapped('amount'), [18.0])
                self.assertEqual(producto.taxes_id.price_include_override, 'tax_included')

    def test_las_facturas_salen_en_soles(self):
        """La lista «Default» de Odoo nace en USD: un cliente sin lista propia no debe facturarse en dólares."""
        soles = self.env.company.currency_id
        self.assertEqual(soles.name, 'PEN')
        self.assertFalse(self.env['product.pricelist'].search([('currency_id', '!=', soles.id)]))
        _pedido, factura = self._facturar(self.cliente_dni)
        self.assertEqual(factura.currency_id, soles)

    def test_los_clientes_nuevos_nacen_en_espanol(self):
        """El PDF de la factura sale en el idioma del cliente."""
        self.assertEqual(self.cliente_ruc.lang, 'es_PE')
        self.assertEqual(self.env['res.partner'].with_context(lang=None).create({'name': 'Cliente sin idioma'}).lang, 'es_PE')

    def test_los_insumos_se_compran_con_igv_18(self):
        insumos = self.env['product.template'].search([
            ('categ_id', 'child_of', self.env.ref('donofrio_base.cat_insumos').id)])
        self.assertTrue(insumos)
        for insumo in insumos:
            with self.subTest(insumo=insumo.default_code):
                self.assertEqual(insumo.supplier_taxes_id.mapped('amount'), [18.0])
                self.assertEqual(insumo.supplier_taxes_id.type_tax_use, 'purchase')

    def test_pedido_con_ruc_factura_en_el_diario_01(self):
        pedido, factura = self._facturar(self.cliente_ruc)
        self.assertEqual(pedido.journal_id, self.facturas)
        self.assertEqual(factura.journal_id, self.facturas)
        self.assertEqual(factura.l10n_latam_document_type_id.code, '01')   # Factura
        self.assertTrue(factura.name.startswith('F '), factura.name)

    def test_pedido_con_dni_factura_en_el_diario_03(self):
        pedido, factura = self._facturar(self.cliente_dni)
        self.assertEqual(pedido.journal_id, self.boletas)
        self.assertEqual(factura.journal_id, self.boletas)
        self.assertEqual(factura.l10n_latam_document_type_id.code, '03')   # Boleta
        self.assertTrue(factura.name.startswith('B '), factura.name)

    def test_consumidor_final_recibe_boleta(self):
        _pedido, factura = self._facturar(self.env.ref('l10n_pe_pos.partner_pe_cf'), cantidad=10)
        self.assertEqual(factura.journal_id, self.boletas)
        self.assertEqual(factura.l10n_latam_document_type_id.code, '03')

    def test_igv_18_correcto(self):
        _pedido, factura = self._facturar(self.cliente_ruc)
        # 100 paletas × S/ 1.50 con IGV incluido = S/ 150.00 → base 127.12 + IGV 22.88
        self.assertAlmostEqual(factura.amount_total, 150.0, places=2)
        self.assertAlmostEqual(factura.amount_untaxed, 150.0 / 1.18, places=2)
        self.assertAlmostEqual(factura.amount_tax, 150.0 - 150.0 / 1.18, places=2)
        self.assertEqual(factura.line_ids.tax_line_id.mapped('amount'), [18.0])

    def test_factura_y_boleta_tienen_informe_pdf_con_igv(self):
        """El informe de la factura es de tipo PDF; aquí se revisa su contenido en HTML.

        El PDF real (wkhtmltopdf) no se genera en las pruebas: pide los estilos al servidor web, que está
        ocupado ejecutando la propia prueba, y se cuelga. Se verifica a mano en la interfaz.
        """
        informe = self.env.ref('account.account_invoices')
        self.assertEqual(informe.report_type, 'qweb-pdf')
        _pedido, factura = self._facturar(self.cliente_ruc)
        _pedido, boleta = self._facturar(self.cliente_dni)
        for documento in (factura, boleta):
            with self.subTest(documento=documento.name):
                html, tipo = self.env['ir.actions.report']._render_qweb_html(informe.id, documento.ids)
                self.assertEqual(tipo, 'html')
                texto = html.decode()
                self.assertIn(documento.name, texto)
                self.assertIn('18%', texto)
