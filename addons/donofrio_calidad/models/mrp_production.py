from odoo import models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        res = super().button_mark_done()
        self._crear_inspecciones()
        return res

    def _crear_inspecciones(self):
        """Al terminar la orden se crea una inspección pendiente por cada lote producido (HU-17)."""
        Inspeccion = self.env['donofrio.calidad.inspeccion'].sudo()
        for prod in self.filtered(lambda p: p.state == 'done'):
            lotes = prod.move_finished_ids.filtered(lambda m: m.product_id == prod.product_id).move_line_ids.lot_id
            for lote in lotes:
                if not Inspeccion.search_count([('production_id', '=', prod.id), ('lot_id', '=', lote.id)]):
                    Inspeccion.create({'production_id': prod.id, 'lot_id': lote.id, 'company_id': prod.company_id.id})
