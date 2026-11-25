from odoo import api, models
from odoo.exceptions import UserError


class ReportCertificado(models.AbstractModel):
    _name = 'report.donofrio_calidad.report_certificado'
    _description = 'Certificado de calidad del lote'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['donofrio.calidad.inspeccion'].browse(docids)
        if docs.filtered(lambda ins: ins.state != 'aprobada'):
            raise UserError(self.env._('El certificado solo se emite para inspecciones aprobadas.'))
        return {'doc_ids': docids, 'doc_model': 'donofrio.calidad.inspeccion', 'docs': docs}
