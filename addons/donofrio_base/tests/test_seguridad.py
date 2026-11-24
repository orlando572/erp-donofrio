import os

from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged

# Rol (xmlid del usuario) → grupos que debe tener, además de los que implican esos grupos
GRUPOS_POR_USUARIO = {
    'user_gerente': {'sales_team.group_sale_salesman_all_leads', 'stock.group_stock_user',
                     'mrp.group_mrp_user', 'account.group_account_readonly'},
    'user_jefe_ventas': {'sales_team.group_sale_manager'},
    'user_vendedor': {'sales_team.group_sale_salesman'},
    'user_cajero_pdv': {'point_of_sale.group_pos_user'},
    'user_jefe_almacen': {'stock.group_stock_manager'},
    'user_jefe_produccion': {'mrp.group_mrp_manager', 'stock.group_stock_user'},
    'user_inspector_calidad': {'stock.group_stock_user'},
    'user_liquidador': {'sales_team.group_sale_salesman', 'stock.group_stock_user',
                        'donofrio_base.group_cd_arequipa'},
    'user_compras': {'purchase.group_purchase_user'},
    'user_contador': {'account.group_account_user'},
}


@tagged('post_install', '-at_install')
class TestSeguridad(TransactionCase):
    """HU-04: usuarios por rol con permisos mínimos y regla de registro del CD Arequipa."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lim = cls.env.ref('stock.warehouse0')
        cls.aqp = cls.env.ref('donofrio_base.wh_aqp')
        cls.liquidador = cls.env.ref('donofrio_base.user_liquidador')
        cls.jefe_almacen = cls.env.ref('donofrio_base.user_jefe_almacen')
        cls.vendedor = cls.env.ref('donofrio_base.user_vendedor')
        cls.cajero = cls.env.ref('donofrio_base.user_cajero_pdv')
        Picking = cls.env['stock.picking']
        cls.picking_lim = Picking.create({
            'picking_type_id': cls.lim.int_type_id.id,
            'location_id': cls.lim.lot_stock_id.id,
            'location_dest_id': cls.env.ref('donofrio_base.loc_lim_congelacion').id,
        })
        cls.picking_aqp = Picking.create({
            'picking_type_id': cls.aqp.int_type_id.id,
            'location_id': cls.aqp.lot_stock_id.id,
            'location_dest_id': cls.env.ref('donofrio_base.loc_aqp_congelacion').id,
        })

    def test_diez_usuarios_con_sus_grupos(self):
        self.assertEqual(len(GRUPOS_POR_USUARIO), 10)
        for xmlid, esperados in GRUPOS_POR_USUARIO.items():
            with self.subTest(usuario=xmlid):
                usuario = self.env.ref(f'donofrio_base.{xmlid}')
                self.assertTrue(usuario.active)
                self.assertTrue(usuario.has_group('base.group_user'))
                for grupo in esperados:
                    self.assertTrue(usuario.has_group(grupo), f'{usuario.login} debería tener {grupo}')

    def test_nadie_es_administrador(self):
        """Mínimo privilegio: ningún usuario por rol es administrador ni de configuración."""
        for xmlid in GRUPOS_POR_USUARIO:
            with self.subTest(usuario=xmlid):
                usuario = self.env.ref(f'donofrio_base.{xmlid}')
                self.assertFalse(usuario.has_group('base.group_system'))
                self.assertFalse(usuario.has_group('base.group_erp_manager'))

    def test_clave_de_prueba_desde_el_entorno(self):
        """La contraseña viene de DONOFRIO_USER_PASSWORD (.env); no está en el código."""
        clave = os.environ.get('DONOFRIO_USER_PASSWORD')
        if not clave:
            self.skipTest('DONOFRIO_USER_PASSWORD no está definida en el entorno')
        usuario = self.env.ref('donofrio_base.user_vendedor')
        info = self.env['res.users'].authenticate(
            {'type': 'password', 'login': usuario.login, 'password': clave}, {'interactive': False})
        self.assertEqual(info['uid'], usuario.id)

    def test_regla_cd_arequipa_en_busquedas(self):
        """El usuario del CD Arequipa solo encuentra las transferencias de su almacén."""
        ids = (self.picking_lim | self.picking_aqp).ids
        vistos = self.env['stock.picking'].with_user(self.liquidador).search([('id', 'in', ids)])
        self.assertEqual(vistos, self.picking_aqp)
        # Control: el jefe de almacén (sin la regla) ve ambas
        vistos_jefe = self.env['stock.picking'].with_user(self.jefe_almacen).search([('id', 'in', ids)])
        self.assertEqual(vistos_jefe, self.picking_lim | self.picking_aqp)

    def test_access_error_en_operacion_de_otro_almacen(self):
        picking_lim = self.picking_lim.with_user(self.liquidador)
        with self.assertRaises(AccessError):
            picking_lim.check_access('read')
        with self.assertRaises(AccessError):
            picking_lim.write({'note': 'no debería poder'})
        # Y sí puede leer la de su almacén
        self.picking_aqp.with_user(self.liquidador).check_access('read')

    def test_regla_en_existencias(self):
        producto = self.env['product.product'].create({
            'name': 'Producto de prueba de seguridad',
            'is_storable': True,
        })
        Quant = self.env['stock.quant']
        q_lim = Quant.create({'product_id': producto.id, 'location_id': self.lim.lot_stock_id.id, 'quantity': 5})
        q_aqp = Quant.create({'product_id': producto.id, 'location_id': self.aqp.lot_stock_id.id, 'quantity': 7})
        vistos = Quant.with_user(self.liquidador).search([('id', 'in', (q_lim | q_aqp).ids)])
        self.assertEqual(vistos, q_aqp)

    def test_vendedor_sin_acceso_a_compras(self):
        with self.assertRaises(AccessError):
            self.env['purchase.order'].with_user(self.vendedor).search([])

    def test_vendedor_no_modifica_almacenes(self):
        """Configurar almacenes es del jefe de almacén (stock.group_stock_manager), no del vendedor."""
        almacenes = self.env['stock.warehouse'].with_user(self.vendedor)
        with self.assertRaises(AccessError):
            almacenes.check_access('write')
        self.env['stock.warehouse'].with_user(self.jefe_almacen).check_access('write')

    def test_cajero_sin_acceso_a_compras(self):
        with self.assertRaises(AccessError):
            self.env['purchase.order'].with_user(self.cajero).search([])
