from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval
from dateutil.relativedelta import relativedelta


@tagged('post_install', '-at_install')
class TestTableroEstandar(TransactionCase):
    """HU-23: dashboards estándar de Community activos y vistas guardadas por código para la gerencia."""

    def _filtro(self, nombre):
        return self.env.ref(f'donofrio_base.{nombre}')

    def _dominio(self, filtro):
        hoy = fields.Date.context_today(self.env['ir.filters'])
        return safe_eval(filtro.domain, {'context_today': lambda: hoy, 'relativedelta': relativedelta})

    def test_dashboards_estandar_publicados(self):
        nombres = set(self.env['spreadsheet.dashboard'].search([('is_published', '=', True)]).mapped('name'))
        for esperado in ('Sales', 'Product', 'Warehouse Metrics', 'Invoicing'):
            with self.subTest(dashboard=esperado):
                self.assertIn(esperado, nombres)

    def test_vistas_guardadas_compartidas_y_ligadas_a_su_pantalla(self):
        esperadas = {
            'filtro_ventas_linea_canal_mes': 'sale.report',
            'filtro_ventas_canal_mes_grafico': 'sale.report',
            'filtro_produccion_por_linea': 'mrp.production',
            'filtro_stock_por_vencer': 'stock.lot',
        }
        for xmlid, modelo in esperadas.items():
            with self.subTest(filtro=xmlid):
                filtro = self._filtro(xmlid)
                self.assertEqual(filtro.model_id, modelo)
                self.assertFalse(filtro.user_ids, 'una vista de gerencia es de todos, no personal')
                self.assertTrue(filtro.action_id)
                accion = self.env[filtro.action_id.type].browse(filtro.action_id.id)
                self.assertEqual(accion.res_model, modelo)

    def test_ventas_por_linea_canal_y_mes_agrupa_con_datos(self):
        filtro = self._filtro('filtro_ventas_linea_canal_mes')
        contexto = safe_eval(filtro.context)
        for campo in contexto['pivot_row_groupby'] + [c.split(':')[0] for c in contexto['pivot_column_groupby']]:
            self.assertIn(campo, self.env['sale.report']._fields, campo)
        for medida in contexto['pivot_measures']:
            self.assertIn(medida, self.env['sale.report']._fields, medida)
        self.assertEqual(contexto['pivot_row_groupby'], ['categ_id', 'team_id'])
        # el dominio y las agrupaciones se ejecutan sin error
        self.env['sale.report'].formatted_read_group(
            safe_eval(filtro.domain), ['categ_id', 'team_id', 'date:month'], ['price_subtotal:sum'])

    def test_produccion_por_producto_y_mes(self):
        filtro = self._filtro('filtro_produccion_por_linea')
        contexto = safe_eval(filtro.context)
        self.assertEqual(contexto['pivot_row_groupby'], ['product_id'])
        self.env['mrp.production'].formatted_read_group(
            safe_eval(filtro.domain), ['product_id', 'date_start:month'], ['product_qty:sum'])

    def test_stock_por_vencer_solo_trae_lotes_con_existencias_que_vencen_en_30_dias(self):
        lote = self._lote_con_stock('LOTE-HU23-PRONTO', dias=10)
        lejano = self._lote_con_stock('LOTE-HU23-LEJANO', dias=200)
        sin_stock = self.env['stock.lot'].create({
            'name': 'LOTE-HU23-SIN-STOCK', 'product_id': lote.product_id.id,
            'expiration_date': fields.Datetime.now() + timedelta(days=5)})
        filtro = self._filtro('filtro_stock_por_vencer')
        encontrados = self.env['stock.lot'].search(self._dominio(filtro))
        self.assertIn(lote, encontrados)
        self.assertNotIn(lejano, encontrados)
        self.assertNotIn(sin_stock, encontrados, 'un lote sin existencias no está «por vencer»')

    def _lote_con_stock(self, nombre, dias):
        producto = self.env.ref('donofrio_base.pt_h01').product_variant_id
        lote = self.env['stock.lot'].create({
            'name': nombre, 'product_id': producto.id,
            'expiration_date': fields.Datetime.now() + timedelta(days=dias)})
        ubicacion = self.env.ref('stock.warehouse0').lot_stock_id
        self.env['stock.quant']._update_available_quantity(producto, ubicacion, 5.0, lot_id=lote)
        return lote
