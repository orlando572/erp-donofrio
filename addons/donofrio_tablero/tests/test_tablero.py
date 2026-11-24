import time
from datetime import timedelta
from unittest.mock import patch

from odoo import Command, fields
from odoo.tests import tagged

from odoo.addons.donofrio_base.tests.common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestTablero(DonofrioStockCase):
    """HU-22 (RF013, CU009): ``get_kpis`` del tablero gerencial."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Tablero = cls.env['donofrio.tablero']
        cls.fresa = cls.env.ref('donofrio_base.pt_h01').product_variant_id
        cls.bom = cls.env.ref('donofrio_base.bom_pt_h01')
        cls.cliente = cls.env['res.partner'].search(
            [('category_id', 'in', cls.env.ref('donofrio_base.cat_heladero').ids)], limit=1)

    def _kpis(self, almacen=False):
        return self.Tablero.get_kpis(warehouse_id=almacen)

    def _pedido(self, cantidad, almacen=None):
        pedido = self.env['sale.order'].create({
            'partner_id': self.cliente.id,
            'warehouse_id': (almacen or self.lim).id,
            'order_line': [Command.create({'product_id': self.fresa.id, 'product_uom_qty': cantidad})],
        })
        pedido.action_confirm()
        return pedido

    # --- Estructura ------------------------------------------------------------------------------------

    def test_estructura_basica(self):
        kpis = self._kpis()
        for clave in ('almacenes', 'almacen_id', 'moneda', 'ventas_mes', 'ventas_por_mes', 'produccion', 'stock_por_vencer'):
            self.assertIn(clave, kpis)
        self.assertEqual({a['id'] for a in kpis['almacenes']}, {self.lim.id, self.aqp.id})
        self.assertFalse(kpis['almacen_id'])
        self.assertEqual(len(kpis['ventas_por_mes']), 6)
        self.assertEqual(kpis['ventas_por_mes'][-1]['mes'], fields.Datetime.now().strftime('%Y-%m'))

    def test_las_tarjetas_opcionales_siguen_a_sus_modulos(self):
        kpis = self._kpis()
        for modelo, clave in (('donofrio.calidad.inspeccion', 'lotes_aprobados'),
                              ('donofrio.liquidacion', 'liquidaciones_pendientes'),
                              ('donofrio.temperatura', 'alertas_temperatura')):
            self.assertEqual(clave in kpis, modelo in self.env, clave)

    def test_sin_los_modulos_opcionales_no_salen_sus_tarjetas(self):
        with patch.object(type(self.Tablero), '_modelo_disponible', return_value=False):
            kpis = self._kpis()
        for clave in ('lotes_aprobados', 'liquidaciones_pendientes', 'alertas_temperatura'):
            self.assertNotIn(clave, kpis)
        self.assertIn('ventas_mes', kpis)

    def test_una_tarjeta_no_sale_si_el_usuario_no_puede_leer_su_modelo(self):
        if 'donofrio.liquidacion' not in self.env:
            self.skipTest('donofrio_heladeros no está instalado')
        sin_acceso = self.env['res.users'].create({
            'name': 'Sin liquidaciones', 'login': 'sin.liquidaciones@example.com',
            'group_ids': [Command.set([self.env.ref('base.group_user').id])]})
        gerente = self.env.ref('donofrio_base.user_gerente')
        self.assertFalse(self.Tablero.with_user(sin_acceso)._modelo_disponible('donofrio.liquidacion'))
        self.assertTrue(self.Tablero.with_user(gerente)._modelo_disponible('donofrio.liquidacion'))
        self.assertFalse(self.Tablero._modelo_disponible('modelo.que.no.existe'))

    def test_lo_abre_el_gerente_con_sus_permisos(self):
        gerente = self.env.ref('donofrio_base.user_gerente')
        kpis = self.Tablero.with_user(gerente).get_kpis()
        self.assertIn('ventas_mes', kpis)

    def test_carga_en_menos_de_3_segundos(self):
        inicio = time.perf_counter()
        self._kpis()
        self.assertLess(time.perf_counter() - inicio, 3.0)

    # --- Ventas ----------------------------------------------------------------------------------------

    def test_las_ventas_del_mes_suman_los_pedidos_confirmados(self):
        antes = self._kpis()
        pedido = self._pedido(10)
        despues = self._kpis()
        self.assertAlmostEqual(despues['ventas_mes']['total'] - antes['ventas_mes']['total'], pedido.amount_total, places=2)
        self.assertAlmostEqual(
            despues['ventas_por_mes'][-1]['total'] - antes['ventas_por_mes'][-1]['total'], pedido.amount_total, places=2)
        canales = {fila['canal'] for fila in despues['ventas_mes']['por_canal']}
        self.assertTrue(canales)

    def test_un_pedido_sin_confirmar_no_cuenta(self):
        antes = self._kpis()['ventas_mes']['total']
        self.env['sale.order'].create({
            'partner_id': self.cliente.id,
            'order_line': [Command.create({'product_id': self.fresa.id, 'product_uom_qty': 5})],
        })
        self.assertEqual(self._kpis()['ventas_mes']['total'], antes)

    def test_el_filtro_por_almacen_separa_las_ventas(self):
        antes_aqp = self._kpis(self.aqp.id)['ventas_mes']['total']
        antes_lim = self._kpis(self.lim.id)['ventas_mes']['total']
        pedido = self._pedido(8, almacen=self.aqp)
        self.assertAlmostEqual(self._kpis(self.aqp.id)['ventas_mes']['total'] - antes_aqp, pedido.amount_total, places=2)
        self.assertAlmostEqual(self._kpis(self.lim.id)['ventas_mes']['total'], antes_lim, places=2)
        self.assertEqual(self._kpis(self.aqp.id)['almacen_id'], self.aqp.id)

    def test_la_variacion_contra_el_mes_anterior(self):
        kpis = self._kpis()['ventas_mes']
        if kpis['anterior']:
            esperado = round((kpis['total'] - kpis['anterior']) / kpis['anterior'] * 100, 1)
            self.assertEqual(kpis['variacion_pct'], esperado)
        else:
            self.assertIsNone(kpis['variacion_pct'])

    # --- Producción ------------------------------------------------------------------------------------

    def test_una_orden_confirmada_cuenta_como_planificada(self):
        antes = self._kpis()['produccion']
        orden = self.env['mrp.production'].create({'product_id': self.fresa.id, 'product_qty': 10, 'bom_id': self.bom.id})
        orden.action_confirm()
        despues = self._kpis()['produccion']
        self.assertEqual(despues['planificadas'], antes['planificadas'] + 1)
        self.assertEqual(despues['hechas'], antes['hechas'])
        self.assertEqual(despues['cumplimiento_pct'], round(despues['hechas'] / despues['planificadas'] * 100, 1))

    def test_sin_ordenes_el_cumplimiento_es_nulo(self):
        with patch.object(type(self.env['mrp.production']), '_read_group', return_value=[]):
            self.assertIsNone(self.Tablero._produccion(fields.Datetime.now(), False)['cumplimiento_pct'])

    # --- Stock por vencer ------------------------------------------------------------------------------

    def test_stock_por_vencer_a_30_dias_y_vencidos(self):
        antes = self._kpis()['stock_por_vencer']
        proximo = self._lote(self.fresa, 'TAB-PROXIMO', 10)
        lejano = self._lote(self.fresa, 'TAB-LEJANO', 90)
        vencido = self._lote(self.fresa, 'TAB-VENCIDO', -3)
        for lote in (proximo, lejano, vencido):
            self._stock(self.fresa, lote, 5)
        despues = self._kpis()['stock_por_vencer']
        self.assertEqual(despues['lotes'], antes['lotes'] + 1)
        self.assertEqual(despues['vencidos'], antes['vencidos'] + 1)
        self.assertAlmostEqual(despues['valor'] - antes['valor'], 5 * self.fresa.standard_price, places=2)
        self.assertEqual(despues['dias'], 30)

    def test_el_stock_por_vencer_respeta_el_almacen(self):
        lote = self._lote(self.fresa, 'TAB-AQP', 5)
        self._stock(self.fresa, lote, 3, ubicacion=self.aqp.lot_stock_id)
        antes_lim = self._kpis(self.lim.id)['stock_por_vencer']['lotes']
        self.assertGreaterEqual(self._kpis(self.aqp.id)['stock_por_vencer']['lotes'], 1)
        self.assertEqual(self._kpis(self.lim.id)['stock_por_vencer']['lotes'], antes_lim)

    # --- Módulos opcionales ----------------------------------------------------------------------------

    def test_lotes_aprobados_de_calidad(self):
        if 'donofrio.calidad.inspeccion' not in self.env:
            self.skipTest('donofrio_calidad no está instalado')
        antes = self._kpis()['lotes_aprobados']
        orden = self.env['mrp.production'].create({'product_id': self.fresa.id, 'product_qty': 10, 'bom_id': self.bom.id})
        for nombre, estado in (('TAB-OK', 'aprobada'), ('TAB-NO', 'rechazada')):
            lote = self._lote(self.fresa, nombre, 100)
            inspeccion = self.env['donofrio.calidad.inspeccion'].create({'production_id': orden.id, 'lot_id': lote.id})
            inspeccion.state = estado
        despues = self._kpis()['lotes_aprobados']
        self.assertEqual(despues['aprobados'], antes['aprobados'] + 1)
        self.assertEqual(despues['inspeccionados'], antes['inspeccionados'] + 2)
        self.assertEqual(despues['aprobados_pct'], round(despues['aprobados'] / despues['inspeccionados'] * 100, 1))

    def test_liquidaciones_pendientes_de_heladeros(self):
        if 'donofrio.liquidacion' not in self.env:
            self.skipTest('donofrio_heladeros no está instalado')
        antes = self._kpis()['liquidaciones_pendientes']['cantidad']
        liquidacion = self.env['donofrio.liquidacion'].create({
            'partner_id': self.cliente.id,
            'linea_ids': [Command.create({'product_id': self.fresa.id, 'despachado': 10, 'devuelto': 2})],
        })
        self.assertEqual(self._kpis()['liquidaciones_pendientes']['cantidad'], antes + 1)
        liquidacion.action_despachar()
        liquidacion.action_confirmar()
        self.assertEqual(self._kpis()['liquidaciones_pendientes']['cantidad'], antes)

    def test_alertas_de_temperatura(self):
        if 'donofrio.temperatura' not in self.env:
            self.skipTest('donofrio_calidad (cadena de frío) no está instalado')
        ubicacion = self.lim.lot_stock_id
        ubicacion.write({'control_temperatura': True, 'temp_min': -25.0, 'temp_max': -18.0})
        antes = self._kpis()['alertas_temperatura']['cantidad']
        self.env['donofrio.temperatura'].create({'location_id': ubicacion.id, 'temperatura': -10.0})
        self.env['donofrio.temperatura'].create({'location_id': ubicacion.id, 'temperatura': -20.0})
        self.assertEqual(self._kpis()['alertas_temperatura']['cantidad'], antes + 1)
        self.assertEqual(self._kpis(self.aqp.id)['alertas_temperatura']['cantidad'], 0)
        vieja = self.env['donofrio.temperatura'].create({
            'location_id': ubicacion.id, 'temperatura': -5.0, 'fecha': fields.Datetime.now() - timedelta(days=30)})
        self.assertTrue(vieja.fuera_de_rango)
        self.assertEqual(self._kpis()['alertas_temperatura']['cantidad'], antes + 1)
