from odoo import Command, api, fields, models
from odoo.exceptions import UserError


class CalidadInspeccion(models.Model):
    """Inspección de un lote terminado (HU-17): mediciones por punto de control, aprobar o rechazar."""
    _name = 'donofrio.calidad.inspeccion'
    _description = 'Inspección de calidad del lote'
    _inherit = ['mail.thread']
    _order = 'id desc'

    _unique_orden_lote = models.Constraint(
        'UNIQUE(production_id, lot_id)', 'Ya existe una inspección para esa orden y ese lote.')

    name = fields.Char('Número', default='/', readonly=True, copy=False)
    production_id = fields.Many2one('mrp.production', 'Orden de producción', required=True, ondelete='restrict', index=True)
    lot_id = fields.Many2one('stock.lot', 'Lote', required=True, ondelete='restrict', index=True)
    product_id = fields.Many2one(related='lot_id.product_id', store=True, string='Producto')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    inspector_id = fields.Many2one('res.users', 'Inspector', tracking=True)
    state = fields.Selection(
        [('borrador', 'Pendiente'), ('en_curso', 'En medición'), ('aprobada', 'Aprobado'), ('rechazada', 'Rechazado')],
        default='borrador', required=True, tracking=True, copy=False)
    linea_ids = fields.One2many('donofrio.calidad.linea', 'inspeccion_id', 'Mediciones')
    motivo_rechazo = fields.Text('Motivo del rechazo')
    todos_cumplen = fields.Boolean(compute='_compute_todos_cumplen')

    @api.depends('linea_ids.resultado')
    def _compute_todos_cumplen(self):
        for ins in self:
            ins.todos_cumplen = bool(ins.linea_ids) and all(l.resultado == 'cumple' for l in ins.linea_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('donofrio.calidad.inspeccion') or '/'
        return super().create(vals_list)

    def _generar_lineas(self):
        """Crea una línea por cada punto de control que aplica al producto del lote."""
        Punto = self.env['donofrio.calidad.punto']
        for ins in self.filtered(lambda i: not i.linea_ids):
            categ = ins.product_id.categ_id
            puntos = Punto.search(['|', ('categ_id', '=', False), ('categ_id', 'parent_of', categ.id)])
            ins.linea_ids = [Command.create({'punto_id': p.id}) for p in puntos]

    def action_iniciar(self):
        for ins in self:
            if ins.state != 'borrador':
                raise UserError(self.env._('Solo se puede iniciar una inspección pendiente.'))
            ins._generar_lineas()
            ins.write({'state': 'en_curso', 'inspector_id': ins.inspector_id.id or self.env.uid})

    def action_aprobar(self):
        for ins in self:
            if ins.state != 'en_curso':
                raise UserError(self.env._('Solo se puede aprobar una inspección en medición.'))
            if not ins.todos_cumplen:
                raise UserError(self.env._('No se puede aprobar: hay puntos de control sin medir o que no cumplen.'))
            ins.state = 'aprobada'

    def action_rechazar(self):
        for ins in self:
            if ins.state != 'en_curso':
                raise UserError(self.env._('Solo se puede rechazar una inspección en medición.'))
            if not ins.motivo_rechazo:
                raise UserError(self.env._('Indica el motivo del rechazo.'))
            ins.state = 'rechazada'
            ins.production_id.message_post(
                body=self.env._('Lote %(lote)s rechazado en la inspección %(ins)s: %(motivo)s. Queda bloqueado para el despacho.',
                                lote=ins.lot_id.name, ins=ins.name, motivo=ins.motivo_rechazo))
            ins.production_id.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=self.env._('Decidir reproceso o descarte del lote %s', ins.lot_id.name),
                user_id=(ins.production_id.user_id or self.env.user).id)


class CalidadLinea(models.Model):
    """Medición de un punto de control dentro de una inspección."""
    _name = 'donofrio.calidad.linea'
    _description = 'Medición de la inspección de calidad'
    _order = 'sequence, id'

    inspeccion_id = fields.Many2one('donofrio.calidad.inspeccion', required=True, ondelete='cascade', index=True)
    punto_id = fields.Many2one('donofrio.calidad.punto', 'Punto de control', required=True, ondelete='restrict')
    sequence = fields.Integer(related='punto_id.sequence', store=True)
    tipo = fields.Selection(related='punto_id.tipo')
    norma = fields.Char(related='punto_id.norma')
    medicion = fields.Float('Medición')
    medido = fields.Boolean('Medido', readonly=True)
    cumple_manual = fields.Boolean('Cumple')
    resultado = fields.Selection(
        [('pendiente', 'Pendiente'), ('cumple', 'Cumple'), ('no_cumple', 'No cumple')],
        compute='_compute_resultado', store=True)

    @api.depends('medicion', 'medido', 'cumple_manual', 'punto_id.tipo', 'punto_id.valor_min', 'punto_id.valor_max')
    def _compute_resultado(self):
        for lin in self:
            punto = lin.punto_id
            if punto.tipo == 'aprobacion':
                lin.resultado = 'cumple' if lin.cumple_manual else 'no_cumple' if lin.medido else 'pendiente'
            elif not lin.medido:
                lin.resultado = 'pendiente'
            else:
                lin.resultado = 'cumple' if punto.valor_min <= lin.medicion <= punto.valor_max else 'no_cumple'

    @api.onchange('medicion', 'cumple_manual')
    def _onchange_medido(self):
        self.medido = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'medicion' in vals or 'cumple_manual' in vals:
                vals.setdefault('medido', True)
        return super().create(vals_list)

    def write(self, vals):
        if ('medicion' in vals or 'cumple_manual' in vals) and 'medido' not in vals:
            vals = dict(vals, medido=True)
        return super().write(vals)
