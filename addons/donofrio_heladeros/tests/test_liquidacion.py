from odoo import Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('post_install', '-at_install')
class TestLiquidacionHeladero(TransactionCase):
    """HU-20 (RF004): liquidación diaria del heladero: vendido, importe, comisión y pedido de venta."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.heladero = cls.env['res.partner'].search(
            [('category_id', 'in', cls.env.ref('donofrio_base.cat_heladero').ids)], limit=1)
        cls.fresa = cls.env.ref('donofrio_base.pt_h01').product_variant_id
        cls.lucuma = cls.env.ref('donofrio_base.pt_h02').product_variant_id
        cls.Liquidacion = cls.env['donofrio.liquidacion']

    def _liquidacion(self, lineas=None, **extra):
        lineas = lineas if lineas is not None else [(self.fresa, 120, 18, 2), (self.lucuma, 80, 10, 0)]
        vals = {
            'partner_id': self.heladero.id,
            'linea_ids': [Command.create({
                'product_id': p.id, 'despachado': d, 'devuelto': v, 'merma': m}) for p, d, v, m in lineas],
        }
        vals.update(extra)
        return self.Liquidacion.create(vals)

    def test_vendido_es_despachado_menos_devuelto_menos_merma(self):
        liq = self._liquidacion()
        fresa, lucuma = liq.linea_ids
        self.assertEqual(fresa.vendido, 100)
        self.assertEqual(lucuma.vendido, 70)
        self.assertEqual(liq.total_vendido, 170)
        self.assertTrue(liq.name.startswith('LIQ/'))

    def test_el_importe_usa_el_precio_de_la_lista_heladero(self):
        liq = self._liquidacion()
        self.assertEqual(liq.pricelist_id, self.env.ref('donofrio_base.lista_heladero'))
        for lin in liq.linea_ids:
            esperado = lin.product_id.list_price * 0.75
            self.assertAlmostEqual(lin.precio_unitario, esperado, places=2)
            self.assertAlmostEqual(lin.importe, esperado * lin.vendido, places=2)
        self.assertAlmostEqual(liq.total_importe, sum(liq.linea_ids.mapped('importe')), places=2)

    def test_comision_y_diferencia_de_efectivo(self):
        liq = self._liquidacion()
        self.assertAlmostEqual(liq.total_comision, liq.total_importe * 0.10, places=2)
        liq.efectivo_entregado = liq.total_importe + 10.5
        self.assertAlmostEqual(liq.diferencia_efectivo, 10.5, places=2)
        liq.porcentaje_comision = 15
        self.assertAlmostEqual(liq.total_comision, liq.total_importe * 0.15, places=2)

    def test_devuelto_mas_merma_no_puede_superar_lo_despachado(self):
        with self.assertRaises(ValidationError):
            self._liquidacion([(self.fresa, 10, 8, 3)])
        liq = self._liquidacion([(self.fresa, 10, 5, 5)])
        self.assertEqual(liq.linea_ids.vendido, 0)

    def test_no_se_aceptan_cantidades_negativas(self):
        with self.assertRaises(Exception), mute_logger('odoo.sql_db'), self.cr.savepoint():
            self._liquidacion([(self.fresa, 10, -1, 0)])

    def test_una_liquidacion_por_heladero_y_dia(self):
        liq = self._liquidacion()
        with self.assertRaises(Exception), mute_logger('odoo.sql_db'), self.cr.savepoint():
            self._liquidacion(fecha=liq.fecha)

    def test_flujo_despachar_y_confirmar_crea_el_pedido(self):
        liq = self._liquidacion([(self.fresa, 120, 18, 2), (self.lucuma, 5, 5, 0)])
        with self.assertRaises(UserError):
            liq.action_confirmar()
        liq.action_despachar()
        self.assertEqual(liq.state, 'despachado')
        liq.action_confirmar()
        self.assertEqual(liq.state, 'liquidado')
        pedido = liq.order_id
        self.assertEqual(pedido.state, 'sale')
        self.assertEqual(pedido.partner_id, self.heladero)
        self.assertEqual(pedido.pricelist_id, liq.pricelist_id)
        self.assertEqual(pedido.origin, liq.name)
        # Solo entra lo vendido; la línea sin unidades vendidas no genera pedido
        self.assertEqual(len(pedido.order_line), 1)
        self.assertEqual(pedido.order_line.product_id, self.fresa)
        self.assertEqual(pedido.order_line.product_uom_qty, 100)
        self.assertAlmostEqual(pedido.order_line.price_unit, self.fresa.list_price * 0.75, places=2)

    def test_no_se_despacha_sin_productos_ni_se_confirma_sin_ventas(self):
        vacia = self._liquidacion([], fecha='2026-01-10')
        with self.assertRaises(UserError):
            vacia.action_despachar()
        sin_ventas = self._liquidacion([(self.fresa, 10, 10, 0)], fecha='2026-01-11')
        sin_ventas.action_despachar()
        with self.assertRaises(UserError):
            sin_ventas.action_confirmar()
        self.assertFalse(sin_ventas.order_id)

    def test_volver_a_borrador_solo_si_esta_despachada(self):
        liq = self._liquidacion()
        with self.assertRaises(UserError):
            liq.action_volver_borrador()
        liq.action_despachar()
        liq.action_volver_borrador()
        self.assertEqual(liq.state, 'borrador')
        liq.action_despachar()
        liq.action_confirmar()
        with self.assertRaises(UserError):
            liq.action_volver_borrador()

    def test_permisos_del_liquidador_y_de_un_usuario_sin_grupo(self):
        liquidador = self.env.ref('donofrio_base.user_liquidador')
        self.assertTrue(liquidador.has_group('donofrio_heladeros.group_heladeros_liquidador'))
        liq = self.Liquidacion.with_user(liquidador).create({
            'partner_id': self.heladero.id,
            'linea_ids': [Command.create({'product_id': self.fresa.id, 'despachado': 10})],
        })
        liq.action_despachar()
        self.assertEqual(liq.state, 'despachado')
        compras = self.env.ref('donofrio_base.user_compras')
        with self.assertRaises(AccessError):
            self.Liquidacion.with_user(compras).create({'partner_id': self.heladero.id})


@tagged('post_install', '-at_install')
class TestPdfLiquidacion(TestLiquidacionHeladero):
    """HU-21 (RF004): PDF de liquidación con el detalle y las firmas; no se imprime en borrador."""

    def _html(self, liq):
        reporte = self.env.ref('donofrio_heladeros.action_report_liquidacion')
        html, _tipo = reporte._render_qweb_html(reporte.report_name, liq.ids)
        return html.decode()

    def test_el_liquidador_por_defecto_es_quien_crea(self):
        liq = self._liquidacion()
        self.assertEqual(liq.liquidador_id, self.env.user)

    def test_pdf_de_una_liquidacion_despachada(self):
        liq = self._liquidacion([(self.fresa, 120, 18, 2)], efectivo_entregado=125.25)
        liq.action_despachar()
        texto = self._html(liq)
        self.assertIn(liq.name, texto)
        self.assertIn(self.heladero.name, texto)
        self.assertIn(self.fresa.display_name, texto)
        self.assertIn('Firma del heladero', texto)
        self.assertIn('Firma del liquidador', texto)
        self.assertIn('a favor del heladero', texto)
        self.assertEqual(liq.action_imprimir()['type'], 'ir.actions.report')

    def test_pdf_cuando_el_heladero_debe(self):
        liq = self._liquidacion([(self.fresa, 10, 0, 0)], efectivo_entregado=1)
        liq.action_despachar()
        self.assertIn('el heladero debe', self._html(liq))

    def test_no_se_imprime_en_borrador(self):
        liq = self._liquidacion()
        reporte = self.env.ref('donofrio_heladeros.action_report_liquidacion')
        with self.assertRaises(UserError):
            reporte._render_qweb_html(reporte.report_name, liq.ids)


@tagged('post_install', '-at_install')
class TestAdministradorHeladeros(TransactionCase):
    """El administrador tiene el grupo de jefatura de Heladeros (incluye al liquidador)."""

    def test_admin_tiene_el_grupo(self):
        admin = self.env.ref('base.user_admin')
        self.assertTrue(admin.has_group('donofrio_heladeros.group_heladeros_jefe'))
        self.assertTrue(admin.has_group('donofrio_heladeros.group_heladeros_liquidador'))
        self.env['donofrio.liquidacion'].with_user(admin).search([], limit=1)
