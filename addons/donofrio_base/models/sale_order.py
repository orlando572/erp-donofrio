from odoo import api, models

RUC = '6'   # código SUNAT del RUC en l10n_pe (l10n_pe_vat_code)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('partner_invoice_id')
    def _compute_journal_id(self):
        """HU-15: el pedido factura en el diario «Facturas» (01) si el cliente tiene RUC y en «Boletas» (03) si no.

        El tipo de documento ya lo elige ``l10n_pe`` según el cliente; esto hace que el diario coincida con él.
        El usuario puede cambiarlo a mano en el pedido.
        """
        super()._compute_journal_id()
        for orden in self:
            orden.journal_id = orden._diario_segun_cliente() or orden.journal_id

    def _diario_segun_cliente(self):
        self.ensure_one()
        if self.company_id.country_id.code != 'PE':
            return self.env['account.journal']
        con_ruc = self.partner_invoice_id.l10n_latam_identification_type_id.l10n_pe_vat_code == RUC
        xmlid = 'donofrio_base.diario_facturas' if con_ruc else 'donofrio_base.diario_boletas'
        return self.env.ref(xmlid, raise_if_not_found=False) or self.env['account.journal']
