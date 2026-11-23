from odoo.tests import tagged

from .common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestReabastecimientoMinMax(DonofrioStockCase):
    """HU-13: la regla mín./máx. genera la RFQ al proveedor, y la OC confirmada crea la recepción."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.insumos = cls.env['product.template'].search([
            ('categ_id', 'child_of', cls.env.ref('donofrio_base.cat_insumos').id)])
        cls.Regla = cls.env['stock.warehouse.orderpoint']
        cls.leche = cls._producto('in_leche')
        cls.regla = cls.env.ref('donofrio_base.rp_leche')

    def _planificar(self, regla):
        """Corre el planificador solo para esta regla, con los mismos pasos que ``stock.rule._run_scheduler_tasks``
        (la tarea programada de Odoo): recalcula lo que hay que pedir y genera las compras."""
        regla = self.Regla.browse(regla.id)
        regla.sudo()._compute_qty_to_order_computed()
        regla.sudo()._procure_orderpoint_confirm(company_id=self.env.company)

    def _rfq(self, producto):
        return self.env['purchase.order.line'].search([
            ('product_id', '=', producto.id), ('order_id.state', '=', 'draft')]).order_id

    def test_cada_insumo_tiene_su_regla_en_lima(self):
        reglas = self.Regla.search([('product_id.product_tmpl_id', 'in', self.insumos.ids)])
        self.assertEqual(len(reglas), len(self.insumos), 'Falta alguna regla de reabastecimiento')
        for regla in reglas:
            with self.subTest(insumo=regla.product_id.default_code):
                self.assertEqual(regla.warehouse_id, self.lim)
                self.assertEqual(regla.location_id, self.lim.lot_stock_id)
                self.assertEqual(regla.route_id, self.env.ref('purchase_stock.route_warehouse0_buy'))
                self.assertEqual(regla.trigger, 'auto')
                self.assertGreater(regla.product_min_qty, 0)
                self.assertGreater(regla.product_max_qty, regla.product_min_qty)
                self.assertTrue(regla.product_id.seller_ids, 'El insumo necesita un proveedor para generar la RFQ')

    def test_bajo_el_minimo_genera_la_rfq_hasta_el_maximo(self):
        self.assertFalse(self._rfq(self.leche))
        self._planificar(self.regla)
        rfq = self._rfq(self.leche)
        self.assertEqual(len(rfq), 1)
        self.assertEqual(rfq.partner_id, self.leche.seller_ids[0].partner_id)
        self.assertEqual(rfq.user_id, self.env.ref('donofrio_base.user_compras'), 'La RFQ debe quedar a cargo del comprador')
        self.assertEqual(rfq.order_line.product_qty, self.regla.product_max_qty)   # sin existencias: se pide hasta el máximo
        self.assertAlmostEqual(rfq.order_line.price_unit, self.leche.seller_ids[0].price)

    def test_con_existencias_sobre_el_minimo_no_genera_rfq(self):
        lote = self._lote(self.leche, 'LECHE-OK', 5)
        self._stock(self.leche, lote, self.regla.product_min_qty + 1)
        self._planificar(self.regla)
        self.assertFalse(self._rfq(self.leche))

    def test_si_ya_hay_una_rfq_en_camino_no_pide_dos_veces(self):
        self._planificar(self.regla)
        self._planificar(self.regla)
        self.assertEqual(len(self._rfq(self.leche)), 1)
        self.assertEqual(self._rfq(self.leche).order_line.product_qty, self.regla.product_max_qty)

    def test_la_oc_confirmada_crea_la_recepcion_en_lima(self):
        self._planificar(self.regla)
        orden = self._rfq(self.leche)
        orden.button_confirm()
        self.assertEqual(orden.state, 'purchase')
        recepcion = orden.picking_ids
        self.assertEqual(len(recepcion), 1)
        self.assertEqual(recepcion.picking_type_id, self.lim.in_type_id)
        self.assertEqual(recepcion.partner_id, orden.partner_id)
        self.assertEqual(recepcion.move_ids.product_id, self.leche)
        self.assertEqual(recepcion.move_ids.product_uom_qty, self.regla.product_max_qty)
        # lo que viene en camino cuenta como previsto: la regla no vuelve a pedir
        self._planificar(self.regla)
        self.assertFalse(self._rfq(self.leche))
