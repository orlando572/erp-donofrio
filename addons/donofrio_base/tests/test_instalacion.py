from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestInstalacion(TransactionCase):
    """Comprueba que el módulo queda instalado (prueba de humo del CI)."""

    def test_modulo_instalado(self):
        modulo = self.env['ir.module.module'].search([('name', '=', 'donofrio_base')])
        self.assertEqual(modulo.state, 'installed')
