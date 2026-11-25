from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    """HU-19 (RF008): rango de temperatura de la ubicación. Antes iba solo en el nombre (Fase 1)."""
    _inherit = 'stock.location'

    control_temperatura = fields.Boolean(
        'Controlar temperatura', copy=False,
        help="Si está marcado, las lecturas de temperatura de esta ubicación se comparan con su rango.")
    temp_min = fields.Float('Temperatura mínima (°C)', copy=False)
    temp_max = fields.Float('Temperatura máxima (°C)', copy=False)

    @api.constrains('control_temperatura', 'temp_min', 'temp_max')
    def _check_rango_temperatura(self):
        for ubicacion in self:
            if ubicacion.control_temperatura and ubicacion.temp_min > ubicacion.temp_max:
                raise ValidationError(self.env._(
                    "En «%(ubicacion)s» la temperatura mínima (%(minima)g °C) no puede ser mayor que la máxima (%(maxima)g °C).",
                    ubicacion=ubicacion.display_name, minima=ubicacion.temp_min, maxima=ubicacion.temp_max))

    @api.model
    def _cargar_rangos_frio(self):
        """Rangos de las cámaras de donofrio_base: congelación −25 °C con producto a −18 °C o menos
        y refrigerado de 2 a 6 °C (supuesto S5). No pisa una ubicación que ya tenga el control activo."""
        rangos = {
            'loc_lim_congelacion': (-30, -18),
            'loc_aqp_congelacion': (-30, -18),
            'loc_lim_refrigerados': (2, 6),
            'loc_aqp_refrigerada': (2, 6),
        }
        for xmlid, (minimo, maximo) in rangos.items():
            ubicacion = self.env.ref(f'donofrio_base.{xmlid}', raise_if_not_found=False)
            if ubicacion and not ubicacion.control_temperatura:
                ubicacion.write({'control_temperatura': True, 'temp_min': minimo, 'temp_max': maximo})
