from odoo import api, models
from odoo.exceptions import UserError


class ReportLiquidacion(models.AbstractModel):
    _name = 'report.donofrio_heladeros.report_liquidacion'
    _description = 'Liquidación del heladero (PDF)'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['donofrio.liquidacion'].browse(docids)
        if docs.filtered(lambda liq: liq.state == 'borrador'):
            raise UserError(self.env._('El PDF se imprime cuando la liquidación está despachada o liquidada.'))
        return {'doc_ids': docids, 'doc_model': 'donofrio.liquidacion', 'docs': docs}
