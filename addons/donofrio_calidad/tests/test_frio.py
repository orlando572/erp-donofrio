from odoo import Command, fields
from odoo.exceptions import AccessError, ValidationError
from odoo.tests import tagged

from odoo.addons.donofrio_base.tests.common import DonofrioStockCase


class CasoFrio(DonofrioStockCase):
    """Utilidades de la cadena de frío (HU-19): cámaras con rango, usuarios por rol y conteo de actividades."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Temperatura = cls.env['donofrio.temperatura']
        cls.camara = cls.env.ref('donofrio_base.loc_lim_refrigerados')   # 2 a 6 °C (datos del módulo)
        cls.sin_rango = cls.env['stock.location'].create({
            'name': 'Almacén seco de prueba', 'usage': 'internal',
            'location_id': cls.lim.lot_stock_id.id})
        cls.jefe = cls.env.ref('donofrio_base.user_jefe_almacen')
        cls.operario = cls.env['res.users'].create({
            'name': 'Operario de cámara', 'login': 'operario.camara@donofrio.example.com',
            'group_ids': [Command.set([cls.env.ref('base.group_user').id, cls.env.ref('stock.group_stock_user').id])]})
        cls.lector = cls.env['res.users'].create({
            'name': 'Usuario interno', 'login': 'lector.frio@donofrio.example.com',
            'group_ids': [Command.set([cls.env.ref('base.group_user').id])]})

    def _lectura(self, grados, ubicacion=None, **extra):
        return self.Temperatura.create({
            'location_id': (ubicacion or self.camara).id, 'temperatura': grados, **extra})

    def _actividades(self, registro, usuario=None):
        dominio = [('res_model', '=', registro._name), ('res_id', '=', registro.id)]
        if usuario:
            dominio.append(('user_id', '=', usuario.id))
        return self.env['mail.activity'].search(dominio)


@tagged('post_install', '-at_install')
class TestTemperatura(CasoFrio):
    """Lecturas de temperatura: marca de fuera de rango y alerta al jefe de almacén."""

    def test_las_camaras_de_la_base_traen_su_rango(self):
        congelacion = self.env.ref('donofrio_base.loc_lim_congelacion')
        self.assertTrue(congelacion.control_temperatura)
        self.assertEqual((congelacion.temp_min, congelacion.temp_max), (-30, -18))
        self.assertEqual((self.camara.temp_min, self.camara.temp_max), (2, 6))

    def test_cargar_rangos_no_pisa_lo_que_se_edito_a_mano(self):
        self.camara.temp_max = 5
        self.env['stock.location']._cargar_rangos_frio()
        self.assertEqual((self.camara.temp_min, self.camara.temp_max), (2, 5))
        self.camara.control_temperatura = False     # como en una base actualizada que aún no tenía el control
        self.env['stock.location']._cargar_rangos_frio()
        self.assertTrue(self.camara.control_temperatura)
        self.assertEqual((self.camara.temp_min, self.camara.temp_max), (2, 6))

    def test_dentro_de_rango_no_alerta(self):
        for grados in (2, 4, 6):    # los extremos están dentro
            lectura = self._lectura(grados)
            self.assertFalse(lectura.fuera_de_rango, grados)
            self.assertFalse(self._actividades(lectura), grados)

    def test_fuera_de_rango_se_marca_y_alerta_al_jefe_de_almacen(self):
        for grados in (6.1, 1.9, 15):
            lectura = self._lectura(grados)
            self.assertTrue(lectura.fuera_de_rango, grados)
            actividades = self._actividades(lectura)
            self.assertEqual(actividades.user_id, self.jefe, grados)
            self.assertEqual(len(actividades), 1)
            self.assertIn(self.camara.display_name, actividades.summary)
            self.assertEqual(lectura.rango, '2 a 6 °C')

    def test_la_ubicacion_sin_rango_no_se_controla(self):
        lectura = self._lectura(40, self.sin_rango)
        self.assertFalse(lectura.fuera_de_rango)
        self.assertFalse(self._actividades(lectura))
        self.assertEqual(lectura.rango, 'Sin rango definido')

    def test_editar_una_lectura_ya_alertada_no_duplica_la_actividad(self):
        lectura = self._lectura(9)
        lectura.observaciones = 'Se abrió la puerta'
        lectura.temperatura = 10
        lectura.write({'fecha': fields.Datetime.now()})
        self.assertTrue(lectura.fuera_de_rango)
        self.assertEqual(len(self._actividades(lectura)), 1)

    def test_si_la_alerta_ya_se_atendio_editar_no_la_vuelve_a_crear(self):
        lectura = self._lectura(9)
        self._actividades(lectura).action_feedback()
        lectura.observaciones = 'Revisado'
        self.assertFalse(self._actividades(lectura))

    def test_corregir_una_lectura_de_dentro_a_fuera_crea_la_actividad_una_vez(self):
        lectura = self._lectura(4)
        self.assertFalse(self._actividades(lectura))
        lectura.temperatura = 8
        self.assertTrue(lectura.fuera_de_rango)
        self.assertEqual(len(self._actividades(lectura)), 1)
        lectura.temperatura = 7
        self.assertEqual(len(self._actividades(lectura)), 1)

    def test_corregir_una_lectura_de_fuera_a_dentro_la_desmarca(self):
        lectura = self._lectura(8)
        lectura.temperatura = 5
        self.assertFalse(lectura.fuera_de_rango)

    def test_cambiar_el_rango_no_reevalua_el_historial(self):
        lectura = self._lectura(7)
        self.assertTrue(lectura.fuera_de_rango)
        self.camara.temp_max = 8
        self.assertTrue(lectura.fuera_de_rango)
        self.assertFalse(self._lectura(7).fuera_de_rango)

    def test_crear_varias_lecturas_a_la_vez(self):
        lecturas = self.Temperatura.create([
            {'location_id': self.camara.id, 'temperatura': 4},
            {'location_id': self.camara.id, 'temperatura': 9},
            {'location_id': self.sin_rango.id, 'temperatura': 30},
        ])
        self.assertEqual(lecturas.mapped('fuera_de_rango'), [False, True, False])
        self.assertEqual(len(self._actividades(lecturas[1])), 1)
        self.assertFalse(self._actividades(lecturas[0]) | self._actividades(lecturas[2]))

    def test_sin_el_jefe_de_demostracion_avisa_a_los_usuarios_del_grupo(self):
        self.jefe.active = False
        destinatarios = self.Temperatura._usuarios_alerta()
        self.assertTrue(destinatarios)
        self.assertNotIn(self.env.ref('base.user_root'), destinatarios)
        self.assertTrue(all(usuario.has_group('stock.group_stock_manager') for usuario in destinatarios))

    def test_el_operario_registra_y_la_alerta_llega_al_jefe(self):
        lectura = self.Temperatura.with_user(self.operario).create({
            'location_id': self.camara.id, 'temperatura': 12})
        self.assertEqual(lectura.user_id, self.operario)
        self.assertEqual(self._actividades(lectura).user_id, self.jefe)

    def test_el_listado_de_lecturas_fuera_de_rango_se_filtra(self):
        buena, mala = self._lectura(3), self._lectura(11)
        fuera = self.Temperatura.search([('fuera_de_rango', '=', True), ('id', 'in', (buena | mala).ids)])
        self.assertEqual(fuera, mala)


@tagged('post_install', '-at_install')
class TestRangoUbicacion(CasoFrio):
    """stock.location: temp_min y temp_max opcionales, con restricción."""

    def test_minimo_mayor_que_maximo_no_se_permite(self):
        with self.assertRaises(ValidationError):
            self.sin_rango.write({'control_temperatura': True, 'temp_min': 5, 'temp_max': 1})
        with self.assertRaises(ValidationError):
            self.camara.temp_min = 7

    def test_minimo_igual_al_maximo_o_sin_control_si_se_permite(self):
        self.sin_rango.write({'control_temperatura': True, 'temp_min': 4, 'temp_max': 4})
        self.sin_rango.write({'control_temperatura': False, 'temp_min': 9, 'temp_max': 1})

    def test_rango_que_incluye_el_cero(self):
        self.sin_rango.write({'control_temperatura': True, 'temp_min': 0, 'temp_max': 4})
        self.assertFalse(self._lectura(0, self.sin_rango).fuera_de_rango)
        self.assertTrue(self._lectura(-0.5, self.sin_rango).fuera_de_rango)


@tagged('post_install', '-at_install')
class TestSeguridadFrio(CasoFrio):
    """ACL de donofrio.temperatura: almacén registra, el jefe borra, los demás solo leen."""

    def test_el_operario_crea_y_edita_pero_no_borra(self):
        lectura = self._lectura(3).with_user(self.operario)
        lectura.observaciones = 'Turno tarde'
        with self.assertRaises(AccessError):
            lectura.unlink()

    def test_el_jefe_de_almacen_borra(self):
        lectura = self._lectura(3).with_user(self.jefe)
        lectura.unlink()
        self.assertFalse(lectura.exists())

    def test_un_usuario_interno_solo_lee(self):
        lectura = self._lectura(3).with_user(self.lector)
        self.assertEqual(lectura.temperatura, 3)
        with self.assertRaises(AccessError):
            lectura.temperatura = 4
        with self.assertRaises(AccessError):
            self.Temperatura.with_user(self.lector).create({'location_id': self.camara.id, 'temperatura': 3})
        with self.assertRaises(AccessError):
            lectura.unlink()


@tagged('post_install', '-at_install')
class TestCronLotesPorVencer(CasoFrio):
    """Cron diario: una actividad, una sola vez, por lote con stock que vence dentro de N días."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.producto = cls.env.ref('donofrio_base.pt_h01').product_variant_id
        cls.parametros = cls.env['ir.config_parameter']
        # Lotes previos de la base (si los hubiera) no deben mezclarse con los de la prueba
        cls.Lote.search([]).write({'alerta_vencimiento_fecha': fields.Datetime.now()})

    def _lote_con_stock(self, nombre, dias, cantidad=10):
        lote = self._lote(self.producto, nombre, dias)
        if cantidad:
            self._stock(self.producto, lote, cantidad)
        return lote

    def test_el_parametro_por_defecto_son_7_dias(self):
        self.assertEqual(self.parametros.get_param('donofrio_calidad.dias_alerta_vencimiento'), '7')
        self.assertEqual(self.Lote._dias_alerta_vencimiento(), 7)

    def test_sin_lotes_por_vencer_no_crea_nada(self):
        self._lote_con_stock('LOTE-LEJANO', 60)
        antes = self.env['mail.activity'].search_count([('res_model', '=', 'stock.lot')])
        self.assertEqual(self.Lote._cron_lotes_por_vencer(), 0)
        self.assertEqual(self.env['mail.activity'].search_count([('res_model', '=', 'stock.lot')]), antes)

    def test_un_lote_con_stock_por_vencer_genera_una_actividad_para_el_jefe(self):
        lote = self._lote_con_stock('LOTE-POR-VENCER', 5)
        self.assertEqual(self.Lote._cron_lotes_por_vencer(), 1)
        actividades = self._actividades(lote)
        self.assertEqual(len(actividades), 1)
        self.assertEqual(actividades.user_id, self.jefe)
        self.assertEqual(actividades.date_deadline, lote.expiration_date.date())
        self.assertTrue(lote.alerta_vencimiento_fecha)

    def test_correr_el_cron_otra_vez_no_duplica_aunque_se_atienda_la_actividad(self):
        lote = self._lote_con_stock('LOTE-UNA-VEZ', 3)
        self.Lote._cron_lotes_por_vencer()
        self.assertEqual(self.Lote._cron_lotes_por_vencer(), 0)
        self.assertEqual(len(self._actividades(lote)), 1)
        self._actividades(lote).action_feedback()
        self.Lote._cron_lotes_por_vencer()
        self.assertFalse(self._actividades(lote))

    def test_no_alerta_lotes_sin_stock_ya_vencidos_ni_fuera_de_ventana(self):
        sin_stock = self._lote_con_stock('LOTE-SIN-STOCK', 2, cantidad=0)
        vencido = self._lote_con_stock('LOTE-VENCIDO', -2)
        lejano = self._lote_con_stock('LOTE-8-DIAS', 8)
        self.assertEqual(self.Lote._cron_lotes_por_vencer(), 0)
        for lote in (sin_stock, vencido, lejano):
            self.assertFalse(self._actividades(lote), lote.name)

    def test_el_parametro_cambia_la_ventana(self):
        lote = self._lote_con_stock('LOTE-10-DIAS', 10)
        self.assertEqual(self.Lote._cron_lotes_por_vencer(), 0)
        self.parametros.set_param('donofrio_calidad.dias_alerta_vencimiento', '15')
        self.assertEqual(self.Lote._cron_lotes_por_vencer(), 1)
        self.assertEqual(len(self._actividades(lote)), 1)

    def test_un_parametro_invalido_vuelve_a_7_dias(self):
        for valor in ('abc', '0', '-3', ''):
            self.parametros.set_param('donofrio_calidad.dias_alerta_vencimiento', valor)
            self.assertEqual(self.Lote._dias_alerta_vencimiento(), 7, valor)

    def test_varios_lotes_se_alertan_cada_uno_una_vez(self):
        lotes = self._lote_con_stock('LOTE-A', 1) | self._lote_con_stock('LOTE-B', 6)
        self.assertEqual(self.Lote._cron_lotes_por_vencer(), 2)
        self.Lote._cron_lotes_por_vencer()
        for lote in lotes:
            self.assertEqual(len(self._actividades(lote)), 1, lote.name)

    def test_el_cron_esta_declarado_y_activo_cada_dia(self):
        cron = self.env.ref('donofrio_calidad.ir_cron_lotes_por_vencer')
        self.assertTrue(cron.active)
        self.assertEqual((cron.interval_number, cron.interval_type), (1, 'days'))
        self.assertEqual(cron.model_id.model, 'stock.lot')
