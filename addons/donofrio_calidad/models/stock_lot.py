import logging
from datetime import timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

PARAM_DIAS_VENCIMIENTO = 'donofrio_calidad.dias_alerta_vencimiento'
DIAS_VENCIMIENTO_POR_DEFECTO = 7


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

    alerta_vencimiento_fecha = fields.Datetime(
        'Alerta de vencimiento enviada', copy=False, readonly=True,
        help="Cuándo se avisó que el lote estaba por vencer; evita repetir la alerta del cron diario.")

    @api.model
    def _dias_alerta_vencimiento(self):
        """Días de anticipación del cron (parámetro del sistema), 7 si falta o no es un entero positivo."""
        valor = self.env['ir.config_parameter'].sudo().get_param(PARAM_DIAS_VENCIMIENTO)
        try:
            dias = int(valor)
        except (TypeError, ValueError):
            return DIAS_VENCIMIENTO_POR_DEFECTO
        return dias if dias > 0 else DIAS_VENCIMIENTO_POR_DEFECTO

    @api.model
    def _cron_lotes_por_vencer(self):
        """HU-19: una actividad para el jefe de almacén, una sola vez por lote, cuando un lote con stock
        vence dentro de N días."""
        dias = self._dias_alerta_vencimiento()
        ahora = fields.Datetime.now()
        todas = self.env['res.company'].sudo().search([]).ids
        lotes = self.sudo().with_context(allowed_company_ids=todas).search([
            ('expiration_date', '>=', ahora),
            ('expiration_date', '<=', ahora + timedelta(days=dias)),
            ('alerta_vencimiento_fecha', '=', False),
            ('product_qty', '>', 0),
        ])
        usuarios = self.env['donofrio.temperatura']._usuarios_alerta()
        for lote in lotes:
            for usuario in usuarios:
                lote.activity_schedule(
                    act_type_xmlid='mail.mail_activity_data_todo',
                    date_deadline=lote.expiration_date.date(),
                    summary=self.env._("Lote por vencer: %(lote)s", lote=lote.display_name),
                    note=self.env._(
                        "El lote %(lote)s de %(producto)s vence el %(fecha)s y aún tiene %(cantidad)g en stock. "
                        "Priorice su salida (FEFO) o decida su destino.",
                        lote=lote.display_name, producto=lote.product_id.display_name,
                        fecha=fields.Date.to_string(lote.expiration_date.date()), cantidad=lote.product_qty),
                    user_id=usuario.id)
        lotes.write({'alerta_vencimiento_fecha': ahora})
        _logger.info("Lotes por vencer en %s días: %s alertados", dias, len(lotes))
        return len(lotes)
