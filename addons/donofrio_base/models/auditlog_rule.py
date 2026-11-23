from odoo import api, models


class AuditlogRule(models.Model):
    _inherit = 'auditlog.rule'

    @api.model
    def _confirmar_reglas_donofrio(self):
        """HU-27: confirma las reglas de auditoría del módulo que sigan en borrador.

        ``set_to_confirmed`` crea un acceso directo «Ver registros» cada vez que corre, así que solo se llama
        para las que aún no están confirmadas. Es idempotente: sirve igual al instalar que en cada ``-u``.
        """
        xmlids = self.env['ir.model.data'].search([
            ('module', '=', 'donofrio_base'), ('model', '=', 'auditlog.rule'),
        ])
        pendientes = self.browse(xmlids.mapped('res_id')).exists().filtered(lambda r: r.state == 'draft')
        pendientes.set_to_confirmed()
