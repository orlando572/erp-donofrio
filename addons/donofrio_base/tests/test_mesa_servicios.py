from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval


@tagged('post_install', '-at_install')
class TestMesaDeServiciosTI(TransactionCase):
    """HU-32 (RNF011): mesa de servicios en Project con tipos de ticket ITIL y SLA por prioridad."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mesa = cls.env.ref('donofrio_base.proyecto_mesa_servicios')
        cls.Tarea = cls.env['project.task']

    def _ticket(self, prioridad='1', **vals):
        return self.Tarea.create({
            'name': 'Ticket de prueba', 'project_id': self.mesa.id, 'priority': prioridad,
            'stage_id': self.env.ref('donofrio_base.etapa_ti_nuevo').id, **vals})

    # --- Proyecto, etapas y etiquetas por código -----------------------------------------------------

    def test_proyecto_con_las_cinco_etapas_en_orden(self):
        etapas = self.mesa.type_ids.sorted('sequence')
        self.assertEqual(etapas.mapped('name'), ['Nuevo', 'En análisis', 'En atención', 'Resuelto', 'Cerrado'])
        self.assertEqual(etapas.mapped('fold'), [False, False, False, False, True], 'solo «Cerrado» va plegada')

    def test_tres_tipos_de_ticket_itil(self):
        etiquetas = {'etiqueta_ti_incidente': 'Incidente', 'etiqueta_ti_solicitud_servicio': 'Solicitud de servicio',
                     'etiqueta_ti_solicitud_acceso': 'Solicitud de acceso'}
        for xmlid, nombre in etiquetas.items():
            with self.subTest(etiqueta=nombre):
                self.assertEqual(self.env.ref(f'donofrio_base.{xmlid}').name, nombre)

    def test_cinco_tickets_de_ejemplo_con_su_tipo(self):
        tickets = self.Tarea.search([('project_id', '=', self.mesa.id)])
        self.assertEqual(len(tickets), 5)
        for ticket in tickets:
            with self.subTest(ticket=ticket.name):
                self.assertEqual(len(ticket.tag_ids), 1, 'cada ticket tiene un tipo ITIL')

    # --- Fecha límite según la prioridad -------------------------------------------------------------

    def test_la_fecha_limite_sale_de_la_prioridad(self):
        esperado = {'3': 4, '2': 8, '1': 72, '0': 120}   # P1 4 h, P2 8 h, P3 3 días, P4 5 días
        for prioridad, horas in esperado.items():
            with self.subTest(prioridad=prioridad):
                ticket = self._ticket(prioridad)
                self.assertEqual(ticket.date_deadline - ticket.create_date, timedelta(hours=horas))

    def test_una_fecha_limite_escrita_a_mano_se_respeta(self):
        fecha = fields.Datetime.now() + timedelta(days=30)
        ticket = self._ticket('3', date_deadline=fecha)
        self.assertEqual(ticket.date_deadline, fecha)

    def test_cambiar_la_prioridad_de_un_ticket_abierto_recalcula_la_fecha_limite(self):
        ticket = self._ticket('0')
        ticket.priority = '3'
        self.assertEqual(ticket.date_deadline - ticket.create_date, timedelta(hours=4))

    def test_una_tarea_de_otro_proyecto_no_recibe_fecha_limite(self):
        otro = self.env['project.project'].create({'name': 'Otro proyecto'})
        tarea = self.Tarea.create({'name': 'Sin SLA', 'project_id': otro.id, 'priority': '3'})
        self.assertFalse(tarea.date_deadline)
        self.assertFalse(tarea.sla_estado)

    # --- Cumplimiento del SLA ------------------------------------------------------------------------

    def test_ticket_abierto_esta_abierto(self):
        self.assertEqual(self._ticket('2').sla_estado, 'abierto')

    def test_cerrar_a_tiempo_cumple_el_sla_y_cerrar_tarde_lo_incumple(self):
        cerrado = self.env.ref('donofrio_base.etapa_ti_cerrado')
        a_tiempo = self._ticket('2')
        a_tiempo.write({'stage_id': cerrado.id})
        self.assertTrue(a_tiempo.date_end, 'al llegar a la etapa plegada Odoo marca la fecha de cierre')
        self.assertEqual(a_tiempo.sla_estado, 'cumplido')

        tarde = self._ticket('3')
        tarde.write({'stage_id': cerrado.id})
        tarde.date_end = tarde.date_deadline + timedelta(hours=1)   # Odoo pone «ahora» al cerrar; se fuerza el retraso
        self.assertEqual(tarde.sla_estado, 'incumplido')

    def test_los_tickets_de_ejemplo_muestran_cumplido_incumplido_y_abierto(self):
        estado = {ticket.name: ticket.sla_estado for ticket in self.Tarea.search([('project_id', '=', self.mesa.id)])}
        self.assertEqual(estado['Tablero gerencial no carga'], 'cumplido')
        self.assertEqual(estado['Alta de un liquidador para la temporada de verano en el CD Arequipa'], 'incumplido')
        self.assertEqual(sum(1 for e in estado.values() if e == 'abierto'), 3)

    def test_pivote_de_cumplimiento_guardado_y_ejecutable(self):
        filtro = self.env.ref('donofrio_base.filtro_mesa_cumplimiento_sla')
        self.assertFalse(filtro.user_ids, 'es de todos, no personal')
        contexto = safe_eval(filtro.context)
        self.assertEqual(contexto['pivot_row_groupby'], ['tag_ids'])
        self.assertEqual(contexto['pivot_column_groupby'], ['sla_estado'])
        grupos = self.Tarea.formatted_read_group(filtro._get_eval_domain(), ['tag_ids', 'sla_estado'], ['__count'])
        self.assertEqual(sum(g['__count'] for g in grupos), 5)
