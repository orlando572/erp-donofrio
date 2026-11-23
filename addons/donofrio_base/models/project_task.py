from datetime import timedelta

from odoo import api, fields, models

# HU-32 (09 §9.3): objetivo de resolución por prioridad de la mesa de servicios TI.
# Las prioridades de Odoo 19 son '0' a '3'; la matriz ITIL del proyecto es P1 a P4.
HORAS_DE_RESOLUCION = {
    '3': 4,       # P1 Crítica (Urgente): 4 h
    '2': 8,       # P2 Alta: 8 h
    '1': 72,      # P3 Media: 3 días
    '0': 120,     # P4 Baja: 5 días
}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sla_estado = fields.Selection(
        [('abierto', 'Abierto'), ('cumplido', 'SLA cumplido'), ('incumplido', 'SLA incumplido')],
        string='Cumplimiento del SLA', compute='_compute_sla_estado', store=True,
        help='Cumplido si el ticket se cerró antes de su fecha límite; incumplido si se cerró después. '
             'Solo se calcula en los tickets con fecha límite.')

    @api.depends('date_deadline', 'date_end')
    def _compute_sla_estado(self):
        for tarea in self:
            if not tarea.date_deadline:
                tarea.sla_estado = False
            elif not tarea.date_end:
                tarea.sla_estado = 'abierto'
            else:
                tarea.sla_estado = 'cumplido' if tarea.date_end <= tarea.date_deadline else 'incumplido'

    def _es_de_la_mesa(self):
        mesa = self.env.ref('donofrio_base.proyecto_mesa_servicios', raise_if_not_found=False)
        return bool(mesa) and self.project_id == mesa

    def _fecha_limite_del_sla(self, inicio=None):
        self.ensure_one()
        inicio = inicio or self.create_date or fields.Datetime.now()
        return inicio + timedelta(hours=HORAS_DE_RESOLUCION[self.priority or '0'])

    @api.model_create_multi
    def create(self, vals_list):
        tareas = super().create(vals_list)
        for tarea, vals in zip(tareas, vals_list):
            if tarea._es_de_la_mesa() and not vals.get('date_deadline'):
                tarea.date_deadline = tarea._fecha_limite_del_sla()
        return tareas

    def write(self, vals):
        resultado = super().write(vals)
        # Si cambia la prioridad de un ticket abierto de la mesa y nadie fijó la fecha, se recalcula desde su creación
        if 'priority' in vals and 'date_deadline' not in vals:
            for tarea in self.filtered(lambda t: t._es_de_la_mesa() and not t.date_end):
                tarea.date_deadline = tarea._fecha_limite_del_sla()
        return resultado
