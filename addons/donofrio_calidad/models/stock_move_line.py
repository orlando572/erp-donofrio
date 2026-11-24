from odoo import models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _action_done(self):
        """Un lote rechazado en calidad no se despacha al cliente (RNF005, CU008)."""
        for ml in self:
            if ml.lot_id and ml.location_dest_id.usage == 'customer' and ml.lot_id.calidad_estado == 'rechazada':
                raise UserError(self.env._(
                    'El lote %s fue rechazado en la inspección de calidad y no se puede despachar.', ml.lot_id.name))
        return super()._action_done()
