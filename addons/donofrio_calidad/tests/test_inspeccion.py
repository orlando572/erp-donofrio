from datetime import timedelta

from odoo import Command, fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged
from odoo.tools import mute_logger

from odoo.addons.donofrio_base.tests.common import DonofrioStockCase


@tagged('post_install', '-at_install')
class TestInspeccionCalidad(DonofrioStockCase):
    """HU-17 (RF011): inspección ligada a la OP y al lote; un lote rechazado no se despacha."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.helado = cls.env.ref('donofrio_base.pt_h01').product_variant_id
        cls.bom = cls.env.ref('donofrio_base.bom_pt_h01')
        for linea in cls.bom.bom_line_ids:
            insumo = linea.product_id
            lote = cls._lote(insumo, f'{insumo.default_code}-CAL', 300) if insumo.tracking == 'lot' else False
            cls._stock(insumo, lote, linea.product_qty * 10)
        cls.Inspeccion = cls.env['donofrio.calidad.inspeccion']

    def _producir(self, cantidad=100):
        orden = self.env['mrp.production'].create({
            'product_id': self.helado.id, 'product_qty': cantidad, 'bom_id': self.bom.id})
        orden.action_confirm()
        orden.action_assign()
        orden.action_generate_serial()
        orden.qty_producing = orden.product_qty
        orden.move_raw_ids.picked = True
        ahora = fields.Datetime.now()
        for operacion in orden.workorder_ids:
            operacion.write({'time_ids': [Command.create({
                'workcenter_id': operacion.workcenter_id.id,
                'loss_id': self.env.ref('mrp.block_reason7').id,
                'date_start': ahora - timedelta(hours=1), 'date_end': ahora})], 'state': 'done'})
        orden.with_context(skip_backorder=True).button_mark_done()
        return orden

    def _inspeccion(self):
        orden = self._producir()
        inspeccion = self.Inspeccion.search([('production_id', '=', orden.id)])
        return orden, inspeccion

    def _medir_todo_bien(self, inspeccion):
        for linea in inspeccion.linea_ids:
            if linea.tipo == 'aprobacion':
                linea.cumple_manual = True
            else:
                linea.medicion = (linea.punto_id.valor_min + linea.punto_id.valor_max) / 2

    def test_al_terminar_la_op_se_crea_la_inspeccion_pendiente(self):
        orden, inspeccion = self._inspeccion()
        self.assertEqual(len(inspeccion), 1)
        self.assertEqual(inspeccion.state, 'borrador')
        self.assertEqual(inspeccion.lot_id, orden.lot_producing_ids)
        self.assertTrue(inspeccion.name.startswith('INS/'))
        self.assertEqual(inspeccion.lot_id.calidad_estado, 'pendiente')

    def test_terminar_otra_vez_no_duplica_la_inspeccion(self):
        orden, inspeccion = self._inspeccion()
        orden._crear_inspecciones()
        self.assertEqual(self.Inspeccion.search_count([('production_id', '=', orden.id)]), 1)

    def test_iniciar_crea_los_puntos_que_aplican_al_producto(self):
        _, inspeccion = self._inspeccion()
        inspeccion.action_iniciar()
        self.assertEqual(inspeccion.state, 'en_curso')
        puntos = inspeccion.linea_ids.punto_id
        self.assertIn(self.env.ref('donofrio_calidad.punto_pasteurizacion'), puntos)
        self.assertIn(self.env.ref('donofrio_calidad.punto_microbiologia'), puntos)
        self.assertNotIn(self.env.ref('donofrio_calidad.punto_humedad_paneton'), puntos)
        self.assertEqual(set(inspeccion.linea_ids.mapped('resultado')), {'pendiente'})

    def test_no_se_aprueba_con_puntos_sin_medir_o_fuera_de_rango(self):
        _, inspeccion = self._inspeccion()
        inspeccion.action_iniciar()
        with self.assertRaises(UserError):
            inspeccion.action_aprobar()
        self._medir_todo_bien(inspeccion)
        pasteurizacion = inspeccion.linea_ids.filtered(lambda l: l.punto_id == self.env.ref('donofrio_calidad.punto_pasteurizacion'))
        pasteurizacion.medicion = 70
        self.assertEqual(pasteurizacion.resultado, 'no_cumple')
        with self.assertRaises(UserError):
            inspeccion.action_aprobar()

    def test_aprobar_con_todo_en_norma(self):
        _, inspeccion = self._inspeccion()
        inspeccion.action_iniciar()
        self._medir_todo_bien(inspeccion)
        self.assertTrue(inspeccion.todos_cumplen)
        inspeccion.action_aprobar()
        self.assertEqual(inspeccion.state, 'aprobada')
        self.assertEqual(inspeccion.lot_id.calidad_estado, 'aprobada')

    def test_rechazar_exige_motivo_y_avisa_a_produccion(self):
        orden, inspeccion = self._inspeccion()
        inspeccion.action_iniciar()
        with self.assertRaises(UserError):
            inspeccion.action_rechazar()
        inspeccion.motivo_rechazo = 'Coliformes sobre la norma'
        inspeccion.action_rechazar()
        self.assertEqual(inspeccion.state, 'rechazada')
        self.assertEqual(inspeccion.lot_id.calidad_estado, 'rechazada')
        self.assertTrue(orden.activity_ids.filtered(lambda a: inspeccion.lot_id.name in (a.summary or '')))

    def _despachar(self, lote):
        cliente = self.env.ref('stock.stock_location_customers')
        picking = self._picking(self.lim.out_type_id, self.lim.lot_stock_id, cliente, self.helado, 5)
        picking.action_assign()
        picking.move_ids.move_line_ids.write({'lot_id': lote.id, 'quantity': 5})
        picking.move_ids.picked = True
        picking.with_context(skip_backorder=True, skip_expired=True).button_validate()
        return picking

    def test_un_lote_rechazado_no_se_despacha(self):
        _, inspeccion = self._inspeccion()
        inspeccion.action_iniciar()
        inspeccion.motivo_rechazo = 'Peso fuera de norma'
        inspeccion.action_rechazar()
        with self.assertRaises(UserError), mute_logger('odoo.sql_db'):
            self._despachar(inspeccion.lot_id)

    def test_un_lote_aprobado_o_sin_inspeccion_se_despacha(self):
        _, inspeccion = self._inspeccion()
        inspeccion.action_iniciar()
        self._medir_todo_bien(inspeccion)
        inspeccion.action_aprobar()
        self.assertEqual(self._despachar(inspeccion.lot_id).state, 'done')

    def test_una_inspeccion_por_orden_y_lote(self):
        orden, inspeccion = self._inspeccion()
        with self.assertRaises(Exception), mute_logger('odoo.sql_db'), self.cr.savepoint():
            self.Inspeccion.create({'production_id': orden.id, 'lot_id': inspeccion.lot_id.id})

    def test_permisos_del_inspector_y_de_un_usuario_sin_grupo(self):
        _, inspeccion = self._inspeccion()
        inspector = self.env.ref('donofrio_base.user_inspector_calidad')
        inspeccion.with_user(inspector).action_iniciar()
        self.assertEqual(inspeccion.state, 'en_curso')
        with self.assertRaises(AccessError):
            self.env['donofrio.calidad.punto'].with_user(inspector).create({'name': 'Prueba', 'tipo': 'aprobacion'})
        sin_grupo = self.env['res.users'].create({
            'name': 'Sin calidad', 'login': 'sin.calidad@example.com',
            'group_ids': [Command.set([self.env.ref('base.group_user').id])]})
        with self.assertRaises(AccessError):
            inspeccion.with_user(sin_grupo).read(['name'])
