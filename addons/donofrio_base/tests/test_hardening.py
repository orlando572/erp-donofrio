from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestEndurecimiento(TransactionCase):
    """HU-27: política de contraseñas, bloqueo por intentos, 2FA de los usuarios privilegiados y auditoría."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.params = cls.env['ir.config_parameter'].sudo()
        cls.admin = cls.env.ref('base.user_admin')
        cls.gerente = cls.env.ref('donofrio_base.user_gerente')
        cls.vendedor = cls.env.ref('donofrio_base.user_vendedor')

    # --- Contraseñas (ISO 27001 5.17) -------------------------------------------------------------------------
    def test_minimo_12_caracteres_configurado(self):
        self.assertEqual(self.params.get_param('auth_password_policy.minlength'), '12')
        self.assertEqual(self.env['res.users'].get_password_policy()['minlength'], 12)

    def test_contrasena_corta_rechazada(self):
        with self.assertRaisesRegex(UserError, '12 characters|12 caracteres'):
            self.vendedor._check_password_policy(['corta-11-ch'])

    def test_contrasena_de_12_o_mas_aceptada(self):
        self.vendedor._check_password_policy(['Donofrio-2026'])  # 13 caracteres: no lanza

    # --- Bloqueo por intentos fallidos (ISO 27001 8.5, OWASP A07) --------------------------------------------
    def test_bloqueo_tras_5_intentos_por_60_s(self):
        self.assertEqual(self.params.get_param('base.login_cooldown_after'), '5')
        self.assertEqual(self.params.get_param('base.login_cooldown_duration'), '60')

    # --- 2FA del administrador y la gerencia (ISO 27001 8.5 y 8.2) --------------------------------------------
    def test_admin_y_gerente_estan_en_el_grupo_2fa_obligatorio(self):
        grupo = self.env.ref('donofrio_base.group_2fa_obligatorio')
        self.assertIn(self.admin, grupo.all_user_ids)
        self.assertIn(self.gerente, grupo.all_user_ids)
        self.assertNotIn(self.vendedor, grupo.all_user_ids)

    def test_2fa_forzada_solo_a_los_privilegiados(self):
        self.params.set_param('donofrio.2fa_privilegiados', 'si')
        self.assertEqual(self.admin._mfa_type(), 'totp_mail')
        self.assertEqual(self.gerente._mfa_type(), 'totp_mail')
        self.assertIsNone(self.vendedor._mfa_type())

    def test_2fa_se_evalua_durante_el_login(self):
        """En el login el entorno es el del usuario público: no debe lanzar AccessError (daba 403 a todos)."""
        self.params.set_param('donofrio.2fa_privilegiados', 'si')
        publico = self.env.ref('base.public_user')
        self.assertEqual(self.admin.with_user(publico)._mfa_type(), 'totp_mail')
        self.assertIsNone(self.vendedor.with_user(publico)._mfa_type())

    def test_2fa_en_modo_auto_depende_del_proxy(self):
        """Sin proxy_mode (desarrollo, CI, pruebas de carga) no se exige: nadie queda fuera por falta de correo."""
        self.params.set_param('donofrio.2fa_privilegiados', 'auto')
        self.assertIsNone(self.admin._mfa_type())
        with patch('odoo.addons.donofrio_base.models.res_users.config', {'proxy_mode': True}):
            self.assertEqual(self.admin._mfa_type(), 'totp_mail')
            self.assertIsNone(self.vendedor._mfa_type())

    def test_2fa_se_puede_apagar(self):
        self.params.set_param('donofrio.2fa_privilegiados', 'no')
        self.assertIsNone(self.admin._mfa_type())

    def test_usuario_con_app_usa_totp(self):
        """Quien ya activó su app de autenticación la usa en lugar del código por correo."""
        self.params.set_param('donofrio.2fa_privilegiados', 'si')
        self.gerente.sudo().totp_secret = 'JBSWY3DPEHPK3PXP'
        self.assertEqual(self.gerente._mfa_type(), 'totp')

    # --- Auditoría de cambios (RNF010) -----------------------------------------------------------------------
    def test_reglas_de_auditoria_confirmadas(self):
        reglas = self.env['auditlog.rule'].search([('id', 'in', [
            self.env.ref(f'donofrio_base.{x}').id for x in (
                'auditlog_rule_pricelist', 'auditlog_rule_pricelist_item',
                'auditlog_rule_sale_order', 'auditlog_rule_purchase_order')])])
        self.assertEqual(len(reglas), 4)
        self.assertEqual(set(reglas.mapped('state')), {'confirmed'})

    def test_cambio_de_precio_queda_auditado(self):
        """Quién, cuándo y valor anterior y nuevo de un cambio en una línea de lista de precios."""
        linea = self.env.ref('donofrio_base.lista_mayorista_regla')
        anterior = linea.percent_price
        linea.with_user(self.env.ref('donofrio_base.user_jefe_ventas')).sudo().write({'percent_price': anterior + 5})
        log = self.env['auditlog.log'].search([
            ('model_id.model', '=', 'product.pricelist.item'), ('res_id', '=', linea.id), ('method', '=', 'write'),
        ], limit=1)
        self.assertTrue(log, 'El cambio de precio no dejó registro de auditoría')
        linea_log = log.line_ids.filtered(lambda x: x.field_name == 'percent_price')
        self.assertEqual(float(linea_log.old_value_text), anterior)
        self.assertEqual(float(linea_log.new_value_text), anterior + 5)
