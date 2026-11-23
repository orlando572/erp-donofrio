from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductosYRecetas(TransactionCase):
    """HU-07: productos terminados, insumos y recetas con operaciones, con lote y vida útil."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Categoria = cls.env['product.category']
        Producto = cls.env['product.template']
        cls.terminados = Producto.search([('categ_id', 'child_of', cls.env.ref('donofrio_base.cat_terminados').id)])
        cls.insumos = Producto.search([('categ_id', 'child_of', cls.env.ref('donofrio_base.cat_insumos').id)])
        cls.categorias = Categoria.search([('id', 'child_of', [
            cls.env.ref('donofrio_base.cat_terminados').id, cls.env.ref('donofrio_base.cat_insumos').id])])
        cls.boms = cls.env['mrp.bom'].search([('product_tmpl_id', 'in', cls.terminados.ids)])

    def test_cantidades(self):
        self.assertEqual(len(self.terminados), 25)
        self.assertEqual(len(self.insumos), 22)
        self.assertEqual(len(self.boms), 12)

    def test_lineas_de_producto(self):
        for linea in ('helados', 'chocolates', 'paneton'):
            with self.subTest(linea=linea):
                categoria = self.env.ref(f'donofrio_base.cat_{linea}')
                self.assertTrue(self.terminados.filtered(lambda p: p.categ_id == categoria))

    def test_terminados_con_lote_y_vida_util(self):
        for producto in self.terminados:
            with self.subTest(producto=producto.default_code):
                self.assertTrue(producto.is_storable)
                self.assertEqual(producto.tracking, 'lot')
                self.assertTrue(producto.use_expiration_date)
                self.assertGreater(producto.expiration_time, 0)
                self.assertEqual(producto.alert_time, 30)
                self.assertTrue(producto.sale_ok)
                self.assertGreater(producto.list_price, producto.standard_price)

    def test_vida_util_por_linea(self):
        """Helado y chocolate 12 meses; panetón 4 meses (03 §3.3 b)."""
        self.assertEqual(self.env.ref('donofrio_base.pt_h01').expiration_time, 365)
        self.assertEqual(self.env.ref('donofrio_base.pt_c01').expiration_time, 365)
        self.assertEqual(self.env.ref('donofrio_base.pt_p01').expiration_time, 120)
        self.assertEqual(self.env.ref('donofrio_base.in_leche').expiration_time, 10)

    def test_insumos_perecibles_con_lote(self):
        perecibles = self.insumos.filtered('use_expiration_date')
        self.assertGreaterEqual(len(perecibles), 15)
        for insumo in perecibles:
            with self.subTest(insumo=insumo.default_code):
                self.assertEqual(insumo.tracking, 'lot')
                self.assertGreater(insumo.expiration_time, 0)
        # El material de empaque no vence ni lleva lote
        self.assertEqual(self.env.ref('donofrio_base.in_envoltura').tracking, 'none')

    def test_insumos_con_proveedor_y_demora(self):
        for insumo in self.insumos:
            with self.subTest(insumo=insumo.default_code):
                self.assertTrue(insumo.purchase_ok)
                self.assertFalse(insumo.sale_ok)
                self.assertTrue(insumo.seller_ids)
                self.assertGreater(insumo.seller_ids[0].delay, 0)

    def test_fefo_en_todas_las_categorias_hoja(self):
        fefo = self.env.ref('product_expiry.removal_fefo')
        hojas = self.categorias.filtered(lambda c: not c.child_id)
        self.assertGreaterEqual(len(hojas), 7)
        for categoria in hojas:
            with self.subTest(categoria=categoria.complete_name):
                self.assertEqual(categoria.removal_strategy_id, fefo)

    def test_recetas_con_componentes_y_operaciones(self):
        for bom in self.boms:
            with self.subTest(receta=bom.product_tmpl_id.default_code):
                self.assertGreater(bom.product_qty, 0)
                self.assertGreaterEqual(len(bom.bom_line_ids), 4)
                self.assertGreaterEqual(len(bom.operation_ids), 3)
                for linea in bom.bom_line_ids:
                    self.assertIn(linea.product_tmpl_id, self.insumos)
                    self.assertGreater(linea.product_qty, 0)
                for operacion in bom.operation_ids:
                    self.assertGreater(operacion.time_cycle_manual, 0)

    def test_tres_centros_de_trabajo(self):
        centros = self.env['mrp.workcenter'].search([('code', 'in', ['LH', 'LC', 'LP'])])
        self.assertEqual(len(centros), 3)
        self.assertTrue(all(c.costs_hour > 0 for c in centros))
        # Cada línea usa su centro: el panetón tiene 5 operaciones en la Línea Panetón
        bom_paneton = self.env.ref('donofrio_base.bom_pt_p01')
        self.assertEqual(len(bom_paneton.operation_ids), 5)
        self.assertEqual(bom_paneton.operation_ids.workcenter_id, self.env.ref('donofrio_base.wc_paneton'))

    def test_pcc_en_las_operaciones(self):
        """Los controles críticos (PCC) quedan documentados en el nombre de la operación."""
        bom = self.env.ref('donofrio_base.bom_pt_h01')
        nombres = ' '.join(bom.operation_ids.mapped('name'))
        self.assertIn('80-85 °C', nombres)
        self.assertIn('-18 °C', nombres)

    def test_lote_calcula_su_vencimiento(self):
        """Al crear un lote, la fecha de vencimiento sale de la vida útil del producto."""
        producto = self.env.ref('donofrio_base.pt_p01').product_variant_id
        lote = self.env['stock.lot'].create({'name': 'LOTE-PRUEBA-P01', 'product_id': producto.id})
        self.assertTrue(lote.expiration_date)
        dias = (lote.expiration_date - fields.Datetime.now()).days
        self.assertIn(dias, (119, 120))
        self.assertAlmostEqual(
            (lote.expiration_date - lote.alert_date).total_seconds(), timedelta(days=30).total_seconds(), delta=60)
