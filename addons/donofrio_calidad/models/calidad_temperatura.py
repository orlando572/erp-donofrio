from odoo import api, fields, models


class Temperatura(models.Model):
    """Lectura de temperatura de una cámara o ubicación de frío (HU-19, RF008, CU006)."""
    _name = 'donofrio.temperatura'
    _description = 'Lectura de temperatura'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha desc, id desc'

    location_id = fields.Many2one(
        'stock.location', 'Ubicación', required=True, index=True, ondelete='restrict', tracking=True,
        domain="[('usage', '=', 'internal')]")
    temperatura = fields.Float('Temperatura (°C)', required=True, tracking=True)
    fecha = fields.Datetime('Fecha y hora', required=True, default=fields.Datetime.now, index=True)
    user_id = fields.Many2one(
        'res.users', 'Registrado por', required=True, default=lambda self: self.env.user, copy=False)
    observaciones = fields.Text('Observaciones')
    temp_min = fields.Float('Mínimo (°C)', related='location_id.temp_min')
    temp_max = fields.Float('Máximo (°C)', related='location_id.temp_max')
    control_temperatura = fields.Boolean(related='location_id.control_temperatura')
    rango = fields.Char('Rango de la ubicación', compute='_compute_rango')
    # Depende solo de la lectura y de la ubicación (no de sus límites): si luego cambia el rango de la
    # ubicación, el historial ya registrado no se reevalúa.
    fuera_de_rango = fields.Boolean(
        'Fuera de rango', compute='_compute_fuera_de_rango', store=True, index=True, tracking=True)
    company_id = fields.Many2one('res.company', related='location_id.company_id', store=True)

    @api.depends('location_id', 'temperatura')
    def _compute_fuera_de_rango(self):
        for lectura in self:
            ubicacion = lectura.location_id
            lectura.fuera_de_rango = bool(
                ubicacion.control_temperatura
                and not ubicacion.temp_min <= lectura.temperatura <= ubicacion.temp_max)

    @api.depends('location_id.control_temperatura', 'location_id.temp_min', 'location_id.temp_max')
    def _compute_rango(self):
        for lectura in self:
            ubicacion = lectura.location_id
            if ubicacion.control_temperatura:
                lectura.rango = f'{ubicacion.temp_min:g} a {ubicacion.temp_max:g} °C'
            else:
                lectura.rango = self.env._('Sin rango definido')

    @api.depends('location_id', 'temperatura', 'fecha')
    def _compute_display_name(self):
        for lectura in self:
            lectura.display_name = f'{lectura.location_id.display_name} · {lectura.temperatura:g} °C'

    @api.model_create_multi
    def create(self, vals_list):
        lecturas = super().create(vals_list)
        lecturas.filtered('fuera_de_rango')._alertar()
        return lecturas

    def write(self, vals):
        antes = {lectura: lectura.fuera_de_rango for lectura in self}
        resultado = super().write(vals)
        # Solo al pasar de dentro a fuera de rango: editar una lectura ya alertada no duplica la actividad
        self.filtered(lambda lectura: lectura.fuera_de_rango and not antes[lectura])._alertar()
        return resultado

    def _usuarios_alerta(self):
        """Quién recibe la alerta: el jefe de almacén (rol stock.group_stock_manager de Inventario).

        Si donofrio_base trae al jefe de almacén de demostración, es él (el administrador también
        pertenece al grupo y no debe recibir todo); si no, los usuarios del grupo, sin OdooBot."""
        jefe = self.env.ref('donofrio_base.user_jefe_almacen', raise_if_not_found=False)
        if jefe and jefe.active:
            return jefe
        grupo = self.env.ref('stock.group_stock_manager')
        return grupo.sudo().all_user_ids.filtered(
            lambda usuario: usuario.active and not usuario.share and usuario != self.env.ref('base.user_root'))

    def _alertar(self):
        """Crea la actividad «fuera de rango» para el jefe de almacén (una por usuario y por lectura)."""
        usuarios = self._usuarios_alerta()
        for lectura in self:
            ya_avisados = lectura.activity_ids.filtered(lambda actividad: actividad.automated).user_id
            for usuario in usuarios - ya_avisados:
                lectura.activity_schedule(
                    act_type_xmlid='mail.mail_activity_data_todo',
                    summary=self.env._(
                        "Temperatura fuera de rango: %(ubicacion)s (%(temperatura)g °C)",
                        ubicacion=lectura.location_id.display_name, temperatura=lectura.temperatura),
                    note=self.env._(
                        "La lectura de %(temperatura)g °C en %(ubicacion)s está fuera de su rango (%(rango)s). "
                        "Revise los lotes almacenados y decida su destino.",
                        temperatura=lectura.temperatura, ubicacion=lectura.location_id.display_name,
                        rango=lectura.rango),
                    user_id=usuario.id)
