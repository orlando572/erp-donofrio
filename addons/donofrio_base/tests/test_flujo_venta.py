from odoo.tests import tagged

from .common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestFlujoDeVenta(DonofrioStockCase):
    """HU-33 (RNF004): pedido → entrega FEFO en pick + ship → factura o boleta con IGV, de punta a punta.

    Junta lo que HU-09 (listas de precios), HU-11 (FEFO), HU-12 (pick + ship) y HU-15 (facturación)
    prueban por separado, para detectar un cambio que rompa la cadena entre ellas.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.helado = cls._producto('pt_h01')                        # S/ 1.50 con IGV incluido
        cls.mayorista = cls.env.ref('donofrio_base.lista_mayorista')   # 15 % menos: S/ 1.275
        cls.facturas = cls.env.ref('donofrio_base.diario_facturas')
        cls.boletas = cls.env.ref('donofrio_base.diario_boletas')
        cls.cliente_ruc = cls.env['res.partner'].create({
            'name': 'Distribuidora de la cadena SAC', 'is_company': True,
            'l10n_latam_identification_type_id': cls.env.ref('l10n_pe.it_RUC').id,
            'vat': '20123456786',
        })
        cls.cliente_dni = cls.env['res.partner'].create({
            'name': 'Cliente de la cadena con DNI',
            'l10n_latam_identification_type_id': cls.env.ref('l10n_pe.it_DNI').id,
            'vat': '12345678',
        })
        # El lote que vence antes se ingresa DESPUÉS: con FIFO saldría primero el otro
        cls.lejano = cls._lote(cls.helado, 'HU33-LEJANO', 300)
        cls._stock(cls.helado, cls.lejano, 100)
        cls.proximo = cls._lote(cls.helado, 'HU33-PROXIMO', 60)
        cls._stock(cls.helado, cls.proximo, 40)

    def _vender(self, cliente, cantidad, lista=None):
        pedido = self.env['sale.order'].create({
            'partner_id': cliente.id,
            'pricelist_id': (lista or self.mayorista).id,
            'order_line': [(0, 0, {'product_id': self.helado.id, 'product_uom_qty': cantidad})],
        })
        pedido.action_confirm()
        return pedido

    def _entregar(self, pedido):
        """Termina el pick y después el ship, como lo haría el almacén. Devuelve (pick, ship).

        El pedido solo crea el pick; Odoo crea el ship (Output → Clientes) al validar el pick.
        """
        pick = pedido.picking_ids.filtered(lambda p: p.picking_type_id == self.lim.pick_type_id)
        self.assertEqual(len(pick), 1, 'Lima despacha en dos pasos: el pedido crea primero el pick')
        self.assertFalse(pedido.picking_ids.filtered(lambda p: p.picking_type_id == self.lim.out_type_id))
        pick.move_ids.picked = True
        pick.button_validate()
        ship = pedido.picking_ids.filtered(lambda p: p.picking_type_id == self.lim.out_type_id)
        self.assertEqual(len(ship), 1, 'Al validar el pick, Odoo crea el ship')
        ship.action_assign()
        ship.move_ids.picked = True
        ship.button_validate()
        return pick, ship

    def _facturar(self, pedido):
        factura = pedido._create_invoices()
        factura.action_post()
        return factura

    def test_pedido_entrega_por_fefo_y_factura_con_ruc(self):
        pedido = self._vender(self.cliente_ruc, 60)

        # 1. El precio sale de la lista mayorista y el pedido crea la entrega en dos pasos
        self.assertAlmostEqual(pedido.order_line.price_unit, 1.275)
        self.assertEqual(pedido.journal_id, self.facturas)
        pick = pedido.picking_ids.filtered(lambda p: p.picking_type_id == self.lim.pick_type_id)
        self.assertEqual(pick.state, 'assigned')

        # 2. FEFO: sale primero el lote que vence antes (40) y se completa con el siguiente (20)
        reservado = {ml.lot_id: ml.quantity for ml in pick.move_ids.move_line_ids}
        self.assertEqual(reservado, {self.proximo: 40, self.lejano: 20})

        # 3. Tras pick y ship, el ship entrega los mismos lotes y baja las existencias
        pick, ship = self._entregar(pedido)
        self.assertEqual((pick.state, ship.state), ('done', 'done'))
        self.assertEqual({ml.lot_id: ml.quantity for ml in ship.move_ids.move_line_ids}, reservado)
        self.assertEqual(pedido.order_line.qty_delivered, 60)
        self.assertEqual(self._disponible(self.helado, self.proximo), 0)
        self.assertEqual(self._disponible(self.helado, self.lejano), 80)

        # 4. Se factura lo entregado: factura (01), diario «Facturas», IGV 18 % incluido en el precio
        factura = self._facturar(pedido)
        self.assertEqual(factura.journal_id, self.facturas)
        self.assertEqual(factura.l10n_latam_document_type_id.code, '01')
        self.assertEqual(factura.currency_id.name, 'PEN')
        self.assertAlmostEqual(factura.amount_total, 76.5, places=2)           # 60 × 1.275
        self.assertAlmostEqual(factura.amount_untaxed, 76.5 / 1.18, places=2)
        self.assertAlmostEqual(factura.amount_tax, 76.5 - 76.5 / 1.18, places=2)
        self.assertEqual(pedido.invoice_status, 'invoiced')

    def test_pedido_de_cliente_con_dni_termina_en_boleta(self):
        pedido = self._vender(self.cliente_dni, 10)
        self._entregar(pedido)

        boleta = self._facturar(pedido)

        self.assertEqual(boleta.journal_id, self.boletas)
        self.assertEqual(boleta.l10n_latam_document_type_id.code, '03')
        self.assertTrue(boleta.name.startswith('B '), boleta.name)
        self.assertAlmostEqual(boleta.amount_total, 12.75, places=2)          # 10 × 1.275

    def test_la_factura_se_puede_pagar_y_queda_cobrada(self):
        pedido = self._vender(self.cliente_ruc, 20)
        self._entregar(pedido)
        factura = self._facturar(pedido)
        self.assertEqual(factura.payment_state, 'not_paid')

        diario_banco = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)
        self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=factura.ids,
        ).create({'journal_id': diario_banco.id}).action_create_payments()

        self.assertIn(factura.payment_state, ('paid', 'in_payment'))
        self.assertEqual(factura.amount_residual, 0)

    def test_un_lote_vencido_no_entra_en_la_entrega_del_pedido(self):
        vencido = self._lote(self.helado, 'HU33-VENCIDO', -5)
        self._stock(self.helado, vencido, 500)

        pedido = self._vender(self.cliente_ruc, 30)
        pick = pedido.picking_ids.filtered(lambda p: p.picking_type_id == self.lim.pick_type_id)

        self.assertNotIn(vencido, pick.move_ids.move_line_ids.lot_id)
        self.assertEqual(sum(pick.move_ids.move_line_ids.mapped('quantity')), 30)
