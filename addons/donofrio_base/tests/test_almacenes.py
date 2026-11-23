from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestAlmacenes(TransactionCase):
    """HU-06: almacenes de Lima y Arequipa con ubicaciones de frío y ruta Lima → Arequipa."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lim = cls.env.ref('stock.warehouse0')
        cls.aqp = cls.env.ref('donofrio_base.wh_aqp')

    def test_dos_almacenes(self):
        almacenes = self.env['stock.warehouse'].search([('company_id', '=', self.env.ref('base.main_company').id)])
        self.assertEqual(set(almacenes.mapped('code')), {'LIM', 'AQP'})
        self.assertEqual(self.lim.name, 'WH-LIM Planta Lima')
        self.assertEqual(self.aqp.name, 'WH-AQP CD Arequipa')

    def test_pasos_de_operacion(self):
        """Despacho en 2 pasos en Lima (pick + ship) y en 1 paso en Arequipa."""
        self.assertEqual(self.lim.delivery_steps, 'pick_ship')
        self.assertTrue(self.lim.pick_type_id.active)
        self.assertEqual(self.aqp.delivery_steps, 'ship_only')
        self.assertEqual(self.lim.reception_steps, 'one_step')
        self.assertEqual(self.aqp.reception_steps, 'one_step')

    def test_ubicaciones_de_frio_y_seco(self):
        esperadas = {
            'donofrio_base.loc_lim_congelacion': ('LIM', 'Cámara de congelación (-25 °C)'),
            'donofrio_base.loc_lim_refrigerados': ('LIM', 'Cámara de insumos refrigerados (2-6 °C)'),
            'donofrio_base.loc_lim_seco': ('LIM', 'Almacén seco'),
            'donofrio_base.loc_lim_despacho_triciclos': ('LIM', 'Zona de despacho de triciclos'),
            'donofrio_base.loc_aqp_congelacion': ('AQP', 'Cámara de congelación (-25 °C)'),
            'donofrio_base.loc_aqp_refrigerada': ('AQP', 'Cámara refrigerada (2-6 °C)'),
            'donofrio_base.loc_aqp_seco': ('AQP', 'Almacén seco'),
            'donofrio_base.loc_aqp_despacho_triciclos': ('AQP', 'Zona de despacho de triciclos'),
        }
        for xmlid, (codigo, nombre) in esperadas.items():
            with self.subTest(ubicacion=xmlid):
                ubicacion = self.env.ref(xmlid)
                self.assertEqual(ubicacion.usage, 'internal')
                self.assertEqual(ubicacion.complete_name, f'{codigo}/Stock/{nombre}')
                self.assertEqual(ubicacion.warehouse_id.code, codigo)

    def test_ruta_lima_arequipa(self):
        self.assertEqual(self.aqp.resupply_wh_ids, self.lim)
        rutas = self.aqp.resupply_route_ids
        self.assertEqual(len(rutas), 1)
        self.assertIn('LIM', rutas.name)
        reglas = rutas.rule_ids
        self.assertIn(self.lim.wh_output_stock_loc_id, reglas.location_src_id)
        self.assertIn(self.aqp.lot_stock_id, reglas.location_dest_id)

    def test_grupos_de_ubicaciones(self):
        grupo_usuario = self.env.ref('base.group_user')
        self.assertIn(self.env.ref('stock.group_stock_multi_locations'), grupo_usuario.implied_ids)
        self.assertIn(self.env.ref('stock.group_adv_location'), grupo_usuario.implied_ids)
