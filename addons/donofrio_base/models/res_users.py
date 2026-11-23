from odoo import models
from odoo.tools import config

# Valores del parámetro «donofrio.2fa_privilegiados»
SI, NO = 'si', 'no'


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _exige_2fa(self):
        """HU-27 (ISO 27001 8.5 y 8.2): el administrador y la gerencia (grupo «2FA obligatorio») usan segundo factor.

        Por defecto («auto») solo se exige en el despliegue protegido (``proxy_mode``), para no bloquear el
        desarrollo, el CI ni las pruebas de carga. El parámetro ``donofrio.2fa_privilegiados`` = ``si`` o ``no`` lo
        fuerza en cualquier entorno.
        """
        self.ensure_one()
        modo = self.env['ir.config_parameter'].sudo().get_param('donofrio.2fa_privilegiados', 'auto')
        activo = modo == SI or (modo != NO and bool(config['proxy_mode']))
        # sudo: durante el login el usuario actual es el público y has_group solo acepta al usuario actual
        return activo and self.sudo().has_group('donofrio_base.group_2fa_obligatorio')

    def _mfa_type(self):
        """Quien ya activó su app de autenticación (TOTP) la usa; quien no, recibe un código por correo
        (``auth_totp_mail``). Requiere un servidor de correo saliente en el despliegue."""
        tipo = super()._mfa_type()
        if tipo is None and self._exige_2fa():
            return 'totp_mail'
        return tipo
