from odoo import fields, models


class CalidadPunto(models.Model):
    """Punto de control de calidad (HU-17): qué se mide y cuál es la norma."""
    _name = 'donofrio.calidad.punto'
    _description = 'Punto de control de calidad'
    _order = 'sequence, id'

    _check_rango = models.Constraint(
        'CHECK(valor_min <= valor_max)', 'El valor mínimo no puede ser mayor que el máximo.')

    name = fields.Char('Punto de control', required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    categ_id = fields.Many2one(
        'product.category', 'Categoría de producto',
        help="Si se deja vacío, el punto se mide en todos los productos.")
    tipo = fields.Selection(
        [('rango', 'Medición dentro de un rango'), ('aprobacion', 'Cumple / no cumple')],
        required=True, default='rango')
    valor_min = fields.Float('Mínimo')
    valor_max = fields.Float('Máximo')
    unidad = fields.Char('Unidad', help="Por ejemplo: °C, g, %.")
    norma = fields.Char('Norma', compute='_compute_norma')

    def _compute_norma(self):
        for punto in self:
            if punto.tipo == 'rango':
                unidad = f' {punto.unidad}' if punto.unidad else ''
                punto.norma = f'{punto.valor_min:g} a {punto.valor_max:g}{unidad}'
            else:
                punto.norma = self.env._('Debe cumplir')
