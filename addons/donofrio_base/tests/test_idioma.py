from odoo.tests import TransactionCase, tagged

from ..models.idioma import TERMINOS_INVENTARIO, UBICACIONES

# Palabras que delatan un texto sin traducir en inventario («Stock» se admite en español)
INGLES = set(TERMINOS_INVENTARIO) | {'Receive', 'Deliver', 'Manufacture', 'Supply', 'Product', 'step', 'steps'}


@tagged('post_install', '-at_install')
class TestIdiomaEspanol(TransactionCase):
    """HU-06: lo que Odoo crea en inglés al instalar (inventario, etapas, listas, etiquetas) se ve en español."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, lang='es_PE', active_test=True))

    def _sin_ingles(self, textos):
        frases = [termino for termino in TERMINOS_INVENTARIO if ' ' in termino]
        for texto in textos:
            with self.subTest(texto=texto):
                palabras = set(texto.replace('(', ' ').replace(')', ' ').split())
                self.assertFalse(palabras & INGLES, texto)
                self.assertFalse([frase for frase in frases if frase in texto], texto)

    def test_tipos_de_operacion_en_espanol(self):
        tipos = self.env['stock.picking.type'].search([])
        self._sin_ingles(tipos.mapped('name'))
        aqp = self.env.ref('donofrio_base.wh_aqp')
        self.assertEqual(aqp.in_type_id.name, 'Recepciones')
        self.assertEqual(aqp.int_type_id.name, 'Traslados internos')
        self.assertEqual(self.env.ref('stock.warehouse0').pick_type_id.name, 'Recoger')

    def test_rutas_y_reglas_en_espanol(self):
        self._sin_ingles(self.env['stock.route'].search([]).mapped('name'))
        self._sin_ingles(self.env['stock.rule'].search([]).mapped('name'))

    def test_ubicaciones_renombradas(self):
        Ubicacion = self.env['stock.location'].with_context(active_test=False)
        self.assertFalse(Ubicacion.search([('name', 'in', list(UBICACIONES))]).mapped('complete_name'))
        self.assertEqual(self.env.ref('stock.stock_location_customers').name, 'Clientes')
        self.assertEqual(self.env.ref('stock.stock_location_suppliers').name, 'Proveedores')

    def test_etapas_personales_del_administrador(self):
        # Odoo las crea al instalar project, cuando todavía no está el español
        etapas = self.env['project.task.type'].search([('user_id', '=', self.env.ref('base.user_admin').id)])
        self.assertFalse(set(etapas.mapped('name')) & {'Inbox', 'Today', 'This Week', 'Later', 'Done', 'Cancelled'})

    def test_lista_por_defecto_y_etiquetas(self):
        self.assertNotIn('Default', self.env['product.pricelist'].with_context(active_test=False).search([]).mapped('name'))
        campos = self.env['ir.model.fields']._get('project.project', 'task_ids')
        self.assertEqual(campos.with_context(lang='es_PE').field_description, 'Tareas')

    def test_es_idempotente(self):
        tipo = self.env.ref('donofrio_base.wh_aqp').in_type_id
        self.env['res.lang']._donofrio_completar_espanol()
        self.env['res.lang']._donofrio_completar_espanol()
        self.assertEqual(tipo.name, 'Recepciones')
        self.assertEqual(tipo.with_context(lang='en_US').name, 'Receipts')
