"""Completa en español (es_PE) los textos que Odoo crea en inglés durante la instalación.

La instalación corre sin idioma (en_US). Los registros que Odoo crea por código en ese momento
(tipos de operación y rutas del almacén de Arequipa, reglas, etapas personales del administrador,
la lista de precios por defecto, impuestos y cuentas de ``l10n_pe``…) guardan solo el texto en inglés,
y la carga del idioma no los traduce porque no vienen de un XML. Aquí se les escribe la versión
en español con los mismos términos de los ``.po`` oficiales de Odoo 19.

Solo se completa lo que no tiene traducción: lo que ya está en español no se toca.
Se ejecuta al instalar y en cada actualización (``data/idioma_data.xml``) y al terminar de cargar
el plan contable (``hooks.py``), porque los impuestos y el PdV se crean después.
"""
import re
from collections import Counter, defaultdict

from odoo import api, models
from odoo.tools import SQL

IDIOMA = 'es_PE'

# Tipos de operación, rutas y reglas (se reemplazan como frases completas, de la más larga a la más corta)
TERMINOS_INVENTARIO = {
    'Deliver in 2 steps (pick + ship)': 'Entregar en 2 pasos (recoger + enviar)',
    'Deliver in 1 step (ship)': 'Entregar en 1 paso (enviar)',
    'Receive in 1 step (stock)': 'Recibir en 1 paso (existencias)',
    'Manufacture (1 step)': 'Fabricación (1 paso)',
    'Supply Product from': 'Abastecer producto desde',
    'Store Finished Product': 'Almacenar producto terminado',
    'Pick Components': 'Recoger componentes',
    'Internal Transfers': 'Traslados internos',
    'Inter-warehouse transit': 'Traslado entre almacenes',
    'Delivery Orders': 'Órdenes de entrega',
    'Quality Control': 'Control de calidad',
    'Manufacturing': 'Fabricación',
    'Pre-Production': 'Preproducción',
    'Production': 'Producción',
    'PoS Orders': 'Pedidos de PdV',
    'Cross Dock': 'Sin almacenaje intermedio (cross dock)',
    'Customers': 'Clientes',
    'Receipts': 'Recepciones',
    'Storage': 'Almacenamiento',
    'Vendors': 'Proveedores',
    'Output': 'Salida',
    '(Buy)': '(Comprar)',
    'Pick': 'Recoger',
    'Pack': 'Empaquetar',
}

# Nombre de las ubicaciones: no es un campo traducible en Odoo 19, así que se renombra.
# «Stock» se deja: es palabra admitida en español y la usan los nombres completos (LIM/Stock/…).
UBICACIONES = {
    'Vendors': 'Proveedores',
    'Customers': 'Clientes',
    'Inter-company transit': 'Tránsito entre compañías',
    'Inter-warehouse transit': 'Traslado entre almacenes',
    'Inventory adjustment': 'Ajuste de inventario',
    'Production': 'Producción',
    'Pre-Production': 'Preproducción',
    'Post-Production': 'Postproducción',
    'Quality Control': 'Control de calidad',
    'Packing Zone': 'Zona de empaquetado',
    'Input': 'Entrada',
    'Output': 'Salida',
}

# Etapas personales de «Tareas pendientes» (las mismas que Odoo crea en español a los demás usuarios)
ETAPAS_PERSONALES = {
    'Inbox': 'Bandeja de entrada',
    'Today': 'Hoy',
    'This Week': 'Esta semana',
    'This Month': 'Este mes',
    'Later': 'Después',
    'Done': 'Hecha',
    'Cancelled': 'Cancelada',
}

# (modelo, campo, {inglés: español}) para textos sueltos
TEXTOS = [
    ('product.pricelist', 'name', {'Default': 'Por defecto'}),
    ('account.tax', 'invoice_label', {
        '18% Free': '18% Libre',
        '-18% Free': '-18% Libre',
        '18% Free Group': '18% Libre Grupo',
    }),
    ('account.reconcile.model.line', 'label', {
        'Internal Transfers': 'Traslados internos',
        'Bank Fees': 'Comisiones bancarias',
    }),
    ('l10n_latam.identification.type', 'description', {
        'Document without RUC from another country': 'Documento sin RUC de otro país',
        'TIN – Doc Trib PP.NN': 'TIN – Doc. tributario PP. NN.',
        'IN - Doc Trib PP. JJ': 'IN – Doc. tributario PP. JJ.',
        'Andean Immigration Card': 'Tarjeta Andina de Migración',
    }),
    ('ir.module.category', 'name', {'Manufacturing': 'Fabricación', 'Localizations': 'Localizaciones'}),
    ('res.groups', 'name', {'Technical Documentation': 'Documentación técnica'}),
    ('project.project', 'label_tasks', {'Tasks': 'Tareas'}),
]

# Etiquetas de campos que Odoo 19 agregó o heredó sin traducción y que no tienen equivalente traducido
# en otro campo (sobre todo de Proyectos). Se ven en filtros personalizados, exportar y agrupar.
ETIQUETAS = {
    '# Collaborators': 'N.º de colaboradores',
    '# Purchase Orders': 'N.º de órdenes de compra',
    '# Tasks': 'N.º de tareas',
    '# of Done Tasks': 'N.º de tareas hechas',
    'Access Instruction Message': 'Mensaje de instrucciones de acceso',
    'Account Reconcile Model Line': 'Línea del modelo de conciliación',
    'Batches': 'Lotes de pago',
    'Bom Count': 'N.º de listas de materiales',
    'Can Be Marked As Done': 'Se puede marcar como hecho',
    'Can Mark Milestone As Done': 'Puede marcar el hito como hecho',
    'Certification Skill Type Count': 'N.º de tipos de habilidad con certificación',
    'Closed Sub-tasks Count': 'N.º de subtareas cerradas',
    'Closed Task Count': 'N.º de tareas cerradas',
    'Closed Task Percentage': 'Porcentaje de tareas cerradas',
    'Current User Same Company Partner': 'Contacto de la misma compañía que el usuario',
    'Dependent Tasks': 'Tareas dependientes',
    'Display Follow Button': 'Mostrar botón de seguir',
    'Display In Project': 'Mostrar en el proyecto',
    'Display Parent Task Button': 'Mostrar botón de tarea principal',
    'Existing Partner': 'Contacto existente',
    'Favorite Projects': 'Proyectos favoritos',
    'Fiscal Country Code of the Company': 'Código del país fiscal de la compañía',
    'Fiscal Year Search': 'Búsqueda por año fiscal',
    'Has Late And Unreached Milestone': 'Tiene un hito atrasado sin alcanzar',
    'Has Project Template': 'Tiene plantilla de proyecto',
    'Has Read Access': 'Tiene acceso de lectura',
    'Installments Mode': 'Modo de cuotas',
    'Is Deadline Exceeded': 'Fecha límite superada',
    'Is Deadline Future': 'Fecha límite futura',
    'Is Milestone Deadline Exceeded': 'Fecha límite del hito superada',
    'Is Milestone Exceeded': 'Hito superado',
    'Is top bar visible': 'Barra superior visible',
    'Kpi Project Task Opened Value': 'KPI de tareas abiertas',
    'Label sanitize': 'Etiqueta depurada',
    'Last Update': 'Última actualización',
    'Last Update Color': 'Color de la última actualización',
    'Last Update Status': 'Estado de la última actualización',
    'Limited Access': 'Acceso limitado',
    'Link Preview Name': 'Nombre de la vista previa del enlace',
    'List order of embedded action ids': 'Orden de las acciones integradas',
    'List visibility of embedded actions ids': 'Visibilidad de las acciones integradas',
    'Log Exports': 'Registrar exportaciones',
    'Log values on deletion': 'Registrar valores al eliminar',
    'Milestone Count': 'N.º de hitos',
    'Milestone Count Reached': 'N.º de hitos alcanzados',
    'Milestones Reached': 'Hitos alcanzados',
    'Name Cropped': 'Nombre recortado',
    'Next Milestone': 'Próximo hito',
    'Number of Projects': 'Número de proyectos',
    'Number of Tasks': 'Número de tareas',
    'Open Installments': 'Cuotas abiertas',
    'Open Installments Preview': 'Vista previa de cuotas abiertas',
    'Open Task Count': 'N.º de tareas abiertas',
    'Personal Stages': 'Etapas personales',
    'Portal User Names': 'Usuarios del portal',
    'Privacy Visibility Warning': 'Aviso de visibilidad',
    'Production Count': 'N.º de producciones',
    'Progress Percentage': 'Porcentaje de avance',
    'Project Allow Milestones': 'El proyecto permite hitos',
    'Project Count': 'N.º de proyectos',
    'Project Shared': 'Proyecto compartido',
    'Rating Request Deadline': 'Fecha límite para pedir valoración',
    'Reached Date': 'Fecha en que se alcanzó',
    'Resource IDs': 'ID de recursos',
    'Sample Dashboard File Path': 'Ruta del tablero de ejemplo',
    'Show Project on Dashboard': 'Mostrar proyecto en el tablero',
    'Show Ratings': 'Mostrar valoraciones',
    'Stage Color': 'Color de la etapa',
    'Stages Active': 'Etapas activas',
    'Stages To Delete': 'Etapas a eliminar',
    'Sub-task Count': 'N.º de subtareas',
    'Sub-tasks': 'Subtareas',
    'Sub-tasks Allocated Time': 'Tiempo asignado a subtareas',
    'Subtask Completion Percentage': 'Porcentaje de subtareas completadas',
    'Task Completion Percentage': 'Porcentaje de tareas completadas',
    'Task Count': 'N.º de tareas',
    'Tasks': 'Tareas',
    'Tasks Stages': 'Etapas de las tareas',
    'Total Employee': 'Total de empleados',
    'Update': 'Actualización',
    'Update Count': 'N.º de actualizaciones',
    'Zip Code': 'Código postal',
}

# Tramos de las cuentas de l10n_pe que no aparecen traducidos en ninguna otra cuenta
TRAMOS_CUENTAS = {'Phone': 'Teléfono'}


def _patron(terminos):
    claves = sorted(terminos, key=len, reverse=True)
    return re.compile('|'.join(r'(?<![\w-])' + re.escape(c) + r'(?![\w-])' for c in claves))


class ResLang(models.Model):
    _inherit = 'res.lang'

    @api.model
    def _donofrio_completar_espanol(self):
        """Escribe en es_PE los textos que solo existen en inglés. Es idempotente."""
        if not self._lang_get(IDIOMA):
            return
        Ubicacion = self.env['stock.location'].with_context(active_test=False)
        for ubicacion in Ubicacion.search([('name', 'in', list(UBICACIONES))]):
            ubicacion.name = UBICACIONES[ubicacion.name]

        patron = _patron(TERMINOS_INVENTARIO)

        def traducir_inventario(texto):
            return patron.sub(lambda coincidencia: TERMINOS_INVENTARIO[coincidencia.group(0)], texto)

        for modelo in ('stock.picking.type', 'stock.route', 'stock.rule'):
            self._donofrio_traducir(self._donofrio_todos(modelo), 'name', traducir_inventario)

        if 'project.task.type' in self.env:
            etapas = self._donofrio_todos('project.task.type', [('user_id', '!=', False)])
            self._donofrio_traducir(etapas, 'name', ETAPAS_PERSONALES.get)

        for modelo, campo, diccionario in TEXTOS:
            if modelo in self.env:
                self._donofrio_traducir(self._donofrio_todos(modelo), campo, diccionario.get)

        if 'account.account' in self.env:
            self._donofrio_traducir_cuentas()
        self._donofrio_traducir_por_coincidencia('ir.model.fields', 'field_description', ETIQUETAS)
        self._donofrio_traducir_por_coincidencia('ir.model.fields', 'help')
        self._donofrio_traducir_por_coincidencia('ir.model.fields.selection', 'name')

    @api.model
    def _donofrio_todos(self, modelo, dominio=()):
        return self.env[modelo].with_context(active_test=False).search(list(dominio))

    @api.model
    def _donofrio_traducir(self, registros, campo, traducir):
        """Pone en es_PE ``traducir(texto_en_inglés)`` donde el campo aún no tiene traducción."""
        for registro in registros:
            ingles = registro.with_context(lang='en_US')[campo]
            if not ingles or registro.with_context(lang=IDIOMA)[campo] != ingles:
                continue  # vacío o ya traducido
            espanol = traducir(ingles)
            if espanol and espanol != ingles:
                registro.update_field_translations(campo, {IDIOMA: espanol})

    @api.model
    def _donofrio_traducir_cuentas(self):
        """Traduce las cuentas por tramos («A - B - C») usando los tramos de las cuentas ya traducidas."""
        Cuenta = self.env['account.account'].with_context(active_test=False)
        tramos = defaultdict(Counter)
        pendientes = Cuenta.browse()
        for cuenta in Cuenta.search([]):
            ingles = cuenta.with_context(lang='en_US').name
            espanol = cuenta.with_context(lang=IDIOMA).name
            if espanol == ingles:
                pendientes |= cuenta
                continue
            partes_en, partes_es = ingles.split(' - '), espanol.split(' - ')
            if len(partes_en) == len(partes_es):
                for tramo_en, tramo_es in zip(partes_en, partes_es):
                    tramos[tramo_en][tramo_es] += 1

        def traducir(texto):
            partes = []
            for tramo in texto.split(' - '):
                if tramo in TRAMOS_CUENTAS:
                    partes.append(TRAMOS_CUENTAS[tramo])
                elif tramos[tramo]:
                    partes.append(tramos[tramo].most_common(1)[0][0])
                else:
                    return None  # tramo desconocido (p. ej. cuentas propias ya escritas en español)
            return ' - '.join(partes)

        self._donofrio_traducir(pendientes, 'name', traducir)

    @api.model
    def _donofrio_traducir_por_coincidencia(self, modelo, campo, propias=None):
        """Etiquetas técnicas sin traducción (campos heredados o nuevos en 19.0 que el .po no trae):
        toma la traducción más usada del mismo texto en otros registros o, si no hay, la de ``propias``.
        Odoo la conserva al actualizar los módulos mientras el texto en inglés no cambie."""
        tabla, columna = SQL.identifier(self.env[modelo]._table), SQL.identifier(campo)
        votos = defaultdict(Counter)
        for ingles, espanol, cantidad in self.env.execute_query(SQL("""
            SELECT %(c)s->>'en_US', %(c)s->>%(idioma)s, count(*)
              FROM %(t)s
             WHERE %(c)s ? %(idioma)s AND %(c)s->>%(idioma)s <> %(c)s->>'en_US'
          GROUP BY 1, 2
        """, c=columna, t=tabla, idioma=IDIOMA)):
            votos[ingles][espanol] += cantidad
        sin_traducir = self.env.execute_query(SQL(
            "SELECT id, %(c)s->>'en_US' FROM %(t)s WHERE NOT %(c)s ? %(idioma)s",
            c=columna, t=tabla, idioma=IDIOMA))
        Modelo = self.env[modelo].sudo()
        cambios = False
        propias = propias or {}
        for registro_id, ingles in sin_traducir:
            espanol = votos[ingles].most_common(1)[0][0] if votos.get(ingles) else propias.get(ingles)
            if espanol:
                Modelo.browse(registro_id).update_field_translations(campo, {IDIOMA: espanol})
                cambios = True
        if cambios:
            # Las etiquetas de los campos se sirven desde la caché «stable» (ir.model.fields._get_fields_cached)
            self.env.registry.clear_cache('stable')
