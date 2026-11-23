from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestEmbudoCrm(TransactionCase):
    """HU-08: embudo CRM por canal, con 3 equipos, 5 etapas y unas 20 oportunidades."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.equipos = cls.env['crm.team'].browse([
            cls.env.ref(f'donofrio_base.equipo_{canal}').id for canal in ('moderno', 'tradicional', 'heladeros')])
        cls.oportunidades = cls.env['crm.lead'].search([
            ('team_id', 'in', cls.equipos.ids), ('type', '=', 'opportunity')])

    def test_tres_equipos_con_jefe(self):
        self.assertEqual(self.equipos.mapped('name'), ['Canal Moderno', 'Canal Tradicional', 'Heladeros'])
        for equipo in self.equipos:
            with self.subTest(equipo=equipo.name):
                self.assertTrue(equipo.user_id)
                self.assertTrue(equipo.use_opportunities)

    def test_cinco_etapas_en_orden(self):
        etapas = self.env['crm.stage'].search([])
        self.assertEqual(etapas.mapped('name'), ['Prospecto', 'Calificado', 'Propuesta', 'Negociación', 'Ganado'])
        self.assertEqual(etapas.filtered('is_won').name, 'Ganado')

    def test_unas_20_oportunidades_en_todas_las_etapas(self):
        self.assertEqual(len(self.oportunidades), 20)
        self.assertEqual(self.oportunidades.stage_id, self.env['crm.stage'].search([]))
        for equipo in self.equipos:
            with self.subTest(equipo=equipo.name):
                self.assertTrue(self.oportunidades.filtered(lambda o: o.team_id == equipo))

    def test_incluye_reclutamiento_de_heladeros(self):
        heladeros = self.oportunidades.filtered(lambda o: o.team_id == self.env.ref('donofrio_base.equipo_heladeros'))
        self.assertTrue(heladeros.filtered(lambda o: 'Reclutamiento' in o.name))

    def test_oportunidad_pasa_a_cotizacion(self):
        oportunidad = self.env.ref('donofrio_base.op_02')
        oportunidad.partner_id = self.env['res.partner'].create({'name': 'Cliente de prueba'})
        accion = oportunidad.action_sale_quotations_new()
        self.assertEqual(accion['res_model'], 'sale.order')
        self.assertEqual(accion['context']['default_opportunity_id'], oportunidad.id)
        cotizacion = self.env['sale.order'].with_context(accion['context']).create({
            'partner_id': oportunidad.partner_id.id,
        })
        self.assertEqual(cotizacion.opportunity_id, oportunidad)
        self.assertEqual(oportunidad.quotation_count, 1)
        cotizacion.action_confirm()
        self.assertEqual(oportunidad.sale_order_count, 1)
