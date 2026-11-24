from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    inspeccion_ids = fields.One2many('donofrio.calidad.inspeccion', 'lot_id', 'Inspecciones de calidad')
    calidad_estado = fields.Selection(
        [('sin_inspeccion', 'Sin inspección'), ('pendiente', 'Pendiente'), ('aprobada', 'Aprobado'), ('rechazada', 'Rechazado')],
        compute='_compute_calidad_estado', string='Calidad')

    @api.depends('inspeccion_ids.state')
    def _compute_calidad_estado(self):
        for lote in self:
            ultima = lote.sudo().inspeccion_ids.sorted('id')[-1:]
            if not ultima:
                lote.calidad_estado = 'sin_inspeccion'
            elif ultima.state in ('aprobada', 'rechazada'):
                lote.calidad_estado = ultima.state
            else:
                lote.calidad_estado = 'pendiente'
