"""HU-16 (ampliación): datos de demostración para las vistas que quedaban vacías o poco creíbles.

Se corre ENCIMA de la base que ya tiene ``cargar_transacciones.py`` (16 semanas, del 3/8 al 22/11/2026) y con
los módulos donofrio_calidad, donofrio_heladeros y donofrio_tablero instalados. No recrea nada. Detén antes el
servicio web: sus tareas programadas corren sobre la misma BD y pueden chocar con el script.

    scripts/backup.sh
    docker compose stop odoo
    docker compose run --rm -T odoo odoo shell -d donofrio --no-http < scripts/cargar_demo_completa.py
    docker compose up -d odoo

Partes (se ejecutan en este orden; cada una hace su propio commit y deja su marca):

* ``contactos``: teléfonos, direcciones y correos en formato peruano para los 63 contactos (y los empleados).
* ``crm``: las 20 oportunidades se enlazan a los clientes reales, se reparten en los tres meses con su
  historial de etapas, actividades hechas, vencidas y pendientes, notas, ganadas (ligadas al pedido) y perdidas
  (con motivo); más 6 oportunidades nuevas.
* ``calidad``: una inspección por cada orden de producción terminada, por los flujos del módulo
  (``_crear_inspecciones``, ``action_iniciar``, ``action_aprobar``, ``action_rechazar``).
* ``heladeros``: una liquidación por cada pedido ya hecho al canal heladeros, cuadrada con ese pedido, con alguna
  merma o diferencia pequeña de efectivo; las del último día quedan pendientes.
* ``frio``: dos lecturas al día en cada cámara durante las 16 semanas, con unos pocos incidentes fuera de rango
  que generan su alerta (actividad para el jefe de almacén).
* ``mesa``: tickets de la mesa de servicios con distintas prioridades y etapas, con su SLA cumplido o incumplido.
* ``calendario``: reuniones en la agenda (semanal de producción, comité mensual, visitas a clientes ligadas a
  las oportunidades, capacitación de heladeros, auditoría, etc.).
* ``fechas``: lleva a la ventana del 3/8 al 22/11 lo que la carga inicial dejó con la fecha de la corrida (25/11):
  asientos de mano de obra de las órdenes de fabricación y de los cierres de Yape del PdV, albaranes del PdV,
  solicitudes de compra del planificador, operaciones de las órdenes, vencimiento de las cotizaciones y los tres
  tickets de la mesa que trae donofrio_base.
* ``ajustes``: textos que Odoo dejó en inglés (tarea de bienvenida del administrador, diario «Point of Sale» y
  referencias de los asientos «Combine … POS payments» y «… - Labour», que Odoo genera en inglés cuando corre
  sin idioma) y los tickets abiertos de la mesa con plazo posterior al 22/11.

Reglas:

* Semilla fija (``SEMILLA``) y fechas fijas dentro del 3/8 al 22/11/2026. ``HOY`` (25/11) es la fecha de
  referencia para saber qué actividades están vencidas y cuáles pendientes.
* Idempotente: cada parte deja un parámetro del sistema ``donofrio_demo_completa.<parte>``; si ya existe, la
  parte no vuelve a cargar. Para repetir una parte, borra su parámetro (o restaura el respaldo).
* ``DONOFRIO_DEMO_PARTES=crm,mesa`` corre solo esas partes (por defecto, todas).
* Todo es ficticio: nombres con ``Ejemplo``, teléfonos con el bloque ``555`` y correos en ``.example.com`` o
  ``.example.pe``. Ninguna persona, correo ni teléfono es real.
"""
import os
import random
from datetime import date, datetime, time, timedelta

from odoo import Command

SEMILLA = 2026
INICIO = date(2026, 8, 3)
FIN = date(2026, 11, 22)
HOY = date(2026, 11, 25)         # fecha de referencia de la demostración (corte del 26/11)
PARAMETRO = 'donofrio_demo_completa.'
PARTES = ('contactos', 'crm', 'calidad', 'heladeros', 'frio', 'mesa', 'calendario', 'fechas', 'ajustes')
PARTES_A_CARGAR = [p for p in os.environ.get('DONOFRIO_DEMO_PARTES', ','.join(PARTES)).split(',') if p]
# La hora de Lima es UTC-5: Odoo guarda las fechas con hora en UTC
DESFASE_LIMA = timedelta(hours=5)


def lima(dia, hora=9, minuto=0):
    """Fecha y hora local de Lima → datetime ingenuo en UTC, como lo guarda Odoo."""
    return datetime.combine(dia, time(hora, minuto)) + DESFASE_LIMA


def ref(env, xmlid):
    return env.ref(f'donofrio_base.{xmlid}')


def usuario(env, xmlid):
    return ref(env, xmlid) if xmlid != 'admin' else env.ref('base.user_admin')


def marca(env, parte):
    return env['ir.config_parameter'].sudo().get_param(PARAMETRO + parte)


def marcar(env, parte):
    env['ir.config_parameter'].sudo().set_param(PARAMETRO + parte, f'{INICIO}..{FIN} semilla {SEMILLA}')


def ultimo_mensaje(env):
    env.cr.execute("SELECT COALESCE(MAX(id), 0) FROM mail_message")
    return env.cr.fetchone()[0]


def fechar_mensajes(env, modelo, res_id, desde, cuando):
    """Pone fecha histórica a los mensajes del historial creados desde ``desde`` (id) en ese registro.

    Antes se vuelcan a la base las escrituras pendientes del ORM (``flush_all``): las de seguimiento crean su
    mensaje al volcar, y si no se hiciera quedarían con la fecha de hoy."""
    env.flush_all()
    env.cr.execute("UPDATE mail_message SET date = %s, create_date = %s WHERE model = %s AND res_id = %s AND id > %s",
                   (cuando, cuando, modelo, res_id, desde))


def conteos(env):
    modelos = ['res.partner', 'crm.lead', 'mail.activity', 'calendar.event', 'project.task',
               'donofrio.calidad.inspeccion', 'donofrio.calidad.linea', 'donofrio.liquidacion',
               'donofrio.liquidacion.linea', 'donofrio.temperatura', 'mail.message']
    return {m: env[m].sudo().with_context(active_test=False).search_count([]) for m in modelos}


# --- Contactos ----------------------------------------------------------------------------------------------

CODIGO_TELEFONICO = {'Lima': '1', 'Callao': '1', 'Arequipa': '54', 'Cusco': '84', 'Puno': '51', 'Tacna': '52',
                     'Trujillo': '44', 'Ica': '56', 'Pucallpa': '61'}
DEPARTAMENTO = {'Lima': 'Lima', 'Callao': 'Callao', 'Arequipa': 'Arequipa', 'Cusco': 'Cusco', 'Puno': 'Puno',
                'Tacna': 'Tacna', 'Trujillo': 'La Libertad', 'Ica': 'Ica', 'Pucallpa': 'Ucayali'}

# nombre → (calle, distrito, código postal, correo); la calle va solo si hay que cambiar la que ya tenía
PROVEEDORES = {
    'Lácteos del Valle Ejemplo SAC': ('Av. Industrial 450, Parque Industrial Río Seco', 'Cerro Colorado', '04014',
                                      'ventas@lacteosdelvalle.example.pe', 'Arequipa'),
    'Cacao y Derivados Ejemplo SAC': ('Av. Los Frutales 1280', 'Ate', '15022', 'comercial@cacaoyderivados.example.pe', 'Lima'),
    'Molino y Azúcar Ejemplo SAC': ('Av. Néstor Gambetta 3560', 'Callao', '07021', 'ventas@molinoyazucar.example.pe', 'Callao'),
    'Frutas y Pulpas Ejemplo SAC': ('Jr. Los Naranjos 342', 'Santa Anita', '15011', 'pedidos@frutasypulpas.example.pe', 'Lima'),
    'Envases y Empaques Ejemplo SAC': ('Av. Separadora Industrial 2150', 'Ate', '15022', 'ventas@envasesyempaques.example.pe', 'Lima'),
    'Cartones y Cajas Ejemplo SAC': ('Calle Los Artesanos 215', 'Villa El Salvador', '15842', 'ventas@cartonesycajas.example.pe', 'Lima'),
}
# partner → (distrito, código postal); la calle que ya traen se conserva
DISTRITOS_CLIENTES = {
    'Distribuidora Andina Ejemplo SAC': ('Wanchaq', '08002'), 'Comercial del Altiplano Ejemplo SAC': ('Puno', '21001'),
    'Distribuidora del Sur Ejemplo SAC': ('Tacna', '23001'), 'Comercial Norte Ejemplo SAC': ('Trujillo', '13001'),
    'Distribuciones Costa Ejemplo SAC': ('Ica', '11001'), 'Comercial Oriente Ejemplo SAC': ('Callería', '25001'),
    'Supermercado Ejemplo SAC': ('San Isidro', '15036'), 'Tiendas Ejemplo Perú SAC': ('San Isidro', '15046'),
    'Minimarket Ejemplo SAC': ('Yanahuara', '04013'), 'Hipermercado del Sur Ejemplo SAC': ('Cercado', '04001'),
    'Cadena Express Ejemplo SAC': ('Jesús María', '15072'), 'Canastas Ejemplo EIRL': ('Miraflores', '15074'),
    'Bodega El Misti Ejemplo EIRL': ('Cercado', '04001'), 'Bodega San Martín Ejemplo EIRL': ('Cayma', '04017'),
    'Bodega Los Andes Ejemplo EIRL': ('Cerro Colorado', '04014'), 'Bodegas Unidas Ejemplo SAC': ('Cercado', '04001'),
    'Mayorista Mercado Ejemplo SAC': ('Cercado', '04001'),
}
# Las bodegas de personas naturales y los heladeros: (calle, distrito, código postal)
DIRECCIONES_ARQUIPA = {
    'Rosa Huamán Quispe (Bodega Santa Rosa)': (None, 'Cercado', '04001'),
    'Marta Flores Ccari (Bodega Villa Hermosa)': (None, 'Paucarpata', '04008'),
    'Luis Mamani Yucra (Bodega La Esperanza)': (None, 'Socabaya', '04015'),
    'Carmen Zapata Rojas (Bodega Cayma)': (None, 'Cayma', '04017'),
    'Pedro Cutipa Huanca (Bodega Umacollo)': (None, 'Yanahuara', '04013'),
    'Luis Alarcón Pinto (heladero Cercado)': ('Calle San Francisco 312', 'Cercado', '04001'),
    'Diego Benavente Soto (heladero Cayma)': ('Av. Ramón Castilla 118', 'Cayma', '04017'),
    'Carmen Delgado Ríos (heladera Yanahuara)': ('Calle Misti 245', 'Yanahuara', '04013'),
    'Raúl Mendoza Cruz (heladero Paucarpata)': ('Av. Kennedy 1480', 'Paucarpata', '04008'),
    'Andrea Ticona Vera (heladera Cerro Colorado)': ('Calle Los Geranios 76', 'Cerro Colorado', '04014'),
    'Ernesto Linares Paz (heladero Socabaya)': ('Av. Socabaya 905', 'Socabaya', '04015'),
    'Silvia Condori Luque (heladera Miraflores)': ('Calle Perú 330', 'Miraflores', '04002'),
    'Walter Quispe Ayala (heladero Sachaca)': ('Av. Sachaca 150', 'Sachaca', '04016'),
}
# Empleados sin usuario: distrito donde viven (dirección del contacto de trabajo no se completa; solo teléfono y correo)
DOMINIO_CORREO = 'donofrio.example.com'


def telefono_fijo(rng, ciudad):
    codigo = CODIGO_TELEFONICO.get(ciudad, '1')
    return f'+51 {codigo} 555 {rng.randint(100, 999):03d}'


def telefono_movil(rng):
    return f'+51 9{rng.randint(10, 99)} 555 {rng.randint(100, 999):03d}'


def sin_tildes(texto):
    for a, b in zip('áéíóúñÁÉÍÓÚÑ', 'aeiounAEIOUN'):
        texto = texto.replace(a, b)
    return texto


def correo_de(nombre):
    palabras = sin_tildes(nombre).lower().replace('(', ' ').replace(')', ' ').split()
    return f'{".".join(palabras[:2])}@{DOMINIO_CORREO}'


def cargar_contactos(env):
    rng = random.Random(SEMILLA + 10)
    Partner = env['res.partner'].with_context(tracking_disable=True, mail_notrack=True)
    estados = {e.name: e for e in env['res.country.state'].search([('country_id.code', '=', 'PE')])}
    peru = env.ref('base.pe')
    n = 0
    for partner in Partner.search([('active', '=', True)], order='id'):
        if partner.id in (1, 2, 3, 4, 5) or partner.vat == '00000000':     # compañía, OdooBot, públicos, consumidor final
            continue
        valores = {}
        ciudad = partner.city or 'Lima'
        if partner.name in PROVEEDORES:
            calle, distrito, zip_, correo, ciudad = PROVEEDORES[partner.name]
            valores.update({'street': calle, 'street2': distrito, 'zip': zip_, 'city': ciudad, 'email': correo})
        elif partner.name in DISTRITOS_CLIENTES:
            distrito, zip_ = DISTRITOS_CLIENTES[partner.name]
            valores.update({'street2': distrito, 'zip': zip_})
        elif partner.name in DIRECCIONES_ARQUIPA:
            calle, distrito, zip_ = DIRECCIONES_ARQUIPA[partner.name]
            valores.update({'street2': distrito, 'zip': zip_, 'city': 'Arequipa'})
            if calle:
                valores['street'] = calle
            ciudad = 'Arequipa'
        if (valores.get('street') or partner.street) and ciudad in DEPARTAMENTO and DEPARTAMENTO[ciudad] in estados \
                and not partner.state_id:
            valores['state_id'] = estados[DEPARTAMENTO[ciudad]].id
        if (valores.get('street') or partner.street) and not partner.country_id:
            valores['country_id'] = peru.id
        if not partner.phone and (partner.is_company or partner.name in PROVEEDORES):
            valores['phone'] = telefono_fijo(rng, ciudad)
        elif not partner.phone:
            valores['phone'] = telefono_movil(rng)
        if not partner.email and not valores.get('email'):
            valores['email'] = correo_de(partner.name)
        partner.write(valores)
        n += 1
    # Empleados: celular y correo de trabajo (los del contacto de trabajo se sincronizan solos)
    empleados = 0
    for empleado in env['hr.employee'].with_context(active_test=False, tracking_disable=True, mail_notrack=True).search([], order='id'):
        valores = {}
        if not empleado.mobile_phone:
            valores['mobile_phone'] = telefono_movil(rng)
        if not empleado.work_phone:
            valores['work_phone'] = '+51 1 555 0100'
        if not empleado.work_email:
            valores['work_email'] = correo_de(empleado.name)
        if valores:
            empleado.write(valores)
            empleados += 1
    print(f'  Contactos: {n} completados, {empleados} empleados con teléfono y correo de trabajo.')


# --- CRM ----------------------------------------------------------------------------------------------------

MOTIVOS_PERDIDA = ['Precio superior al de la competencia', 'Sin línea de crédito aprobada',
                   'Compró a otro proveedor', 'Desistió del proyecto']

# Oportunidades: nombre → cliente, estado final, fecha de alta, etapas con su fecha, cierre, motivo, prioridad, cierre esperado
#   etapas: Prospecto → Calificado → Propuesta → Negociación → Ganado
OPORTUNIDADES = {
    'Distribución regional Cusco': dict(
        cliente='Distribuidora Andina Ejemplo SAC', final='ganada', alta=date(2026, 8, 24),
        etapas=[('calificado', date(2026, 8, 31)), ('propuesta', date(2026, 9, 8)), ('negociacion', date(2026, 9, 16))],
        cierre=date(2026, 9, 24), prioridad='2'),
    'Surtido de helados para autoservicio': dict(
        cliente='Supermercado Ejemplo SAC', final='ganada', alta=date(2026, 9, 1),
        etapas=[('calificado', date(2026, 9, 7)), ('propuesta', date(2026, 9, 15))],
        cierre=date(2026, 9, 29), prioridad='2'),
    'Distribución regional Puno': dict(
        cliente='Comercial del Altiplano Ejemplo SAC', final='perdida', alta=date(2026, 9, 10),
        etapas=[('calificado', date(2026, 9, 17)), ('propuesta', date(2026, 9, 28))],
        cierre=date(2026, 10, 14), motivo=0, prioridad='1'),
    'Campaña de panetón en cadena de tiendas': dict(
        cliente='Tiendas Ejemplo Perú SAC', final='abierta', alta=date(2026, 10, 12),
        etapas=[('calificado', date(2026, 10, 19)), ('propuesta', date(2026, 11, 2)), ('negociacion', date(2026, 11, 17))],
        esperado=date(2026, 12, 4), prioridad='3', pendiente='vencida'),
    'Helados y chocolates para minimarkets': dict(
        cliente='Minimarket Ejemplo SAC', final='abierta', alta=date(2026, 10, 20),
        etapas=[('calificado', date(2026, 10, 27)), ('propuesta', date(2026, 11, 9))],
        esperado=date(2026, 12, 11), prioridad='2', pendiente='futura'),
    'Distribución regional Tacna': dict(
        cliente='Distribuidora del Sur Ejemplo SAC', final='ganada', alta=date(2026, 8, 26),
        etapas=[('calificado', date(2026, 9, 2)), ('propuesta', date(2026, 9, 14)), ('negociacion', date(2026, 10, 1))],
        cierre=date(2026, 10, 12), prioridad='2'),
    'Panetón para canastas corporativas': dict(
        cliente='Canastas Ejemplo EIRL', final='abierta', alta=date(2026, 11, 3),
        etapas=[('calificado', date(2026, 11, 10))],
        esperado=date(2026, 12, 15), prioridad='1', pendiente='futura'),
    'Bodega Santa Rosa': dict(
        cliente='Rosa Huamán Quispe (Bodega Santa Rosa)', final='abierta', alta=date(2026, 10, 27),
        etapas=[('calificado', date(2026, 11, 4)), ('propuesta', date(2026, 11, 12)), ('negociacion', date(2026, 11, 19))],
        esperado=date(2026, 12, 2), prioridad='1', pendiente='vencida'),
    'Bodega Los Andes': dict(
        cliente='Bodega Los Andes Ejemplo EIRL', final='abierta', alta=date(2026, 10, 30),
        etapas=[('calificado', date(2026, 11, 6)), ('propuesta', date(2026, 11, 16))],
        esperado=date(2026, 12, 9), prioridad='1', pendiente='futura'),
    'Bodega San Martín': dict(
        cliente='Bodega San Martín Ejemplo EIRL', final='abierta', alta=date(2026, 11, 9),
        etapas=[('calificado', date(2026, 11, 18))],
        esperado=date(2026, 12, 18), prioridad='0', pendiente='futura'),
    'Mayorista del mercado central': dict(
        cliente='Mayorista Mercado Ejemplo SAC', final='perdida', alta=date(2026, 9, 21),
        etapas=[('calificado', date(2026, 9, 29)), ('propuesta', date(2026, 10, 9))],
        cierre=date(2026, 10, 27), motivo=1, prioridad='2'),
    'Bodega Villa Hermosa': dict(
        cliente='Marta Flores Ccari (Bodega Villa Hermosa)', final='abierta', alta=date(2026, 11, 16),
        etapas=[], esperado=date(2026, 12, 20), prioridad='0', pendiente='futura'),
    'Bodega El Misti': dict(
        cliente='Bodega El Misti Ejemplo EIRL', final='abierta', alta=date(2026, 10, 15),
        etapas=[('calificado', date(2026, 10, 22)), ('propuesta', date(2026, 11, 3)), ('negociacion', date(2026, 11, 13))],
        esperado=date(2026, 11, 30), prioridad='2', pendiente='vencida'),
    'Panetón para bodegas de la zona norte': dict(
        cliente='Bodegas Unidas Ejemplo SAC', final='perdida', alta=date(2026, 10, 5),
        etapas=[('calificado', date(2026, 10, 13)), ('propuesta', date(2026, 10, 21))],
        cierre=date(2026, 11, 6), motivo=2, prioridad='1'),
    'Reclutamiento de heladero, Cercado': dict(
        cliente='Luis Alarcón Pinto (heladero Cercado)', final='ganada', alta=date(2026, 8, 3),
        etapas=[('calificado', date(2026, 8, 5))], cierre=date(2026, 8, 7), prioridad='1', pedido_tras=date(2026, 8, 7)),
    'Reclutamiento de heladero, Cayma': dict(
        cliente='Diego Benavente Soto (heladero Cayma)', final='ganada', alta=date(2026, 8, 4),
        etapas=[('calificado', date(2026, 8, 6))], cierre=date(2026, 8, 10), prioridad='1', pedido_tras=date(2026, 8, 10)),
    'Reclutamiento de heladero, Yanahuara': dict(
        cliente='Carmen Delgado Ríos (heladera Yanahuara)', final='perdida', alta=date(2026, 9, 7),
        etapas=[('calificado', date(2026, 9, 11))], cierre=date(2026, 9, 25), motivo=3, prioridad='0'),
    'Reclutamiento de heladero, Paucarpata': dict(
        cliente='Raúl Mendoza Cruz (heladero Paucarpata)', final='ganada', alta=date(2026, 9, 14),
        etapas=[('calificado', date(2026, 9, 18))], cierre=date(2026, 10, 2), prioridad='1', pedido_tras=date(2026, 10, 2)),
    'Heladero concesionario, Cerro Colorado': dict(
        cliente='Andrea Ticona Vera (heladera Cerro Colorado)', final='ganada', alta=date(2026, 10, 1),
        etapas=[('calificado', date(2026, 10, 6)), ('propuesta', date(2026, 10, 13))],
        cierre=date(2026, 10, 22), prioridad='2', pedido_tras=date(2026, 10, 22)),
    'Heladero concesionario, Socabaya': dict(
        cliente='Ernesto Linares Paz (heladero Socabaya)', final='ganada', alta=date(2026, 10, 8),
        etapas=[('calificado', date(2026, 10, 14)), ('propuesta', date(2026, 10, 23))],
        cierre=date(2026, 11, 3), prioridad='2', pedido_tras=date(2026, 11, 3)),
}
# Oportunidades nuevas: nombre → datos, más equipo, vendedor, ingreso esperado y etiqueta
OPORTUNIDADES_NUEVAS = {
    'Reposición de panetón, Hipermercado del Sur': dict(
        cliente='Hipermercado del Sur Ejemplo SAC', final='abierta', alta=date(2026, 11, 2), etapas=[
            ('calificado', date(2026, 11, 9)), ('propuesta', date(2026, 11, 18))],
        esperado=date(2026, 12, 7), prioridad='3', pendiente='futura', equipo='equipo_moderno', vendedor='user_jefe_ventas',
        ingreso=48000.0),
    'Helados para eventos, Cadena Express': dict(
        cliente='Cadena Express Ejemplo SAC', final='abierta', alta=date(2026, 11, 11), etapas=[
            ('calificado', date(2026, 11, 19))],
        esperado=date(2026, 12, 22), prioridad='1', pendiente='futura', equipo='equipo_moderno', vendedor='user_jefe_ventas',
        ingreso=21000.0),
    'Chocolates para el norte, Comercial Norte': dict(
        cliente='Comercial Norte Ejemplo SAC', final='perdida', alta=date(2026, 9, 15), etapas=[
            ('calificado', date(2026, 9, 23)), ('propuesta', date(2026, 10, 6))],
        cierre=date(2026, 10, 20), motivo=0, prioridad='1', equipo='equipo_moderno', vendedor='user_jefe_ventas',
        ingreso=33000.0),
    'Distribución regional Ica': dict(
        cliente='Distribuciones Costa Ejemplo SAC', final='ganada', alta=date(2026, 8, 12), etapas=[
            ('calificado', date(2026, 8, 19)), ('propuesta', date(2026, 8, 31)), ('negociacion', date(2026, 9, 9))],
        cierre=date(2026, 9, 18), prioridad='2', equipo='equipo_moderno', vendedor='user_jefe_ventas', ingreso=36000.0),
    'Distribución regional Pucallpa': dict(
        cliente='Comercial Oriente Ejemplo SAC', final='abierta', alta=date(2026, 11, 13), etapas=[],
        esperado=date(2026, 12, 28), prioridad='1', pendiente='vencida', equipo='equipo_moderno', vendedor='user_jefe_ventas',
        ingreso=29000.0),
    'Bodega La Esperanza': dict(
        cliente='Luis Mamani Yucra (Bodega La Esperanza)', final='ganada', alta=date(2026, 9, 28), etapas=[
            ('calificado', date(2026, 10, 3)), ('propuesta', date(2026, 10, 12))],
        cierre=date(2026, 10, 19), prioridad='1', equipo='equipo_tradicional', vendedor='user_vendedor', ingreso=3900.0),
}
ETAPA = {'prospecto': 'etapa_prospecto', 'calificado': 'etapa_calificado', 'propuesta': 'etapa_propuesta',
         'negociacion': 'etapa_negociacion', 'ganado': 'etapa_ganado'}
PROBABILIDAD = {'prospecto': 10.0, 'calificado': 25.0, 'propuesta': 50.0, 'negociacion': 75.0}

# Actividades hechas al avanzar de etapa, y notas
ACTIVIDADES_HECHAS = {
    'calificado': [('mail.mail_activity_data_call', 'Llamada de presentación',
                    'Se presentó la línea de helados, chocolates y panetón; el cliente pide la lista de precios.'),
                   ('mail.mail_activity_data_email', 'Enviar catálogo y lista de precios',
                    'Catálogo y lista de precios enviados por correo.')],
    'propuesta': [('mail.mail_activity_data_meeting', 'Visita comercial',
                   'Visita realizada: se revisaron volúmenes, frecuencia de entrega y condiciones de pago.'),
                  ('mail.mail_activity_data_email', 'Enviar propuesta comercial',
                   'Propuesta enviada con la lista de precios vigente y el plazo de entrega.')],
    'negociacion': [('mail.mail_activity_data_call', 'Negociar plazo de pago',
                     'El cliente pide 30 días de crédito; se consulta con el jefe de ventas.'),
                    ('mail.mail_activity_data_upload_document', 'Enviar fichas técnicas y certificados de calidad',
                     'Fichas técnicas y certificados de calidad de los lotes enviados.')],
}
ACTIVIDADES_PENDIENTES = {
    'futura': [('mail.mail_activity_data_call', 'Llamar para confirmar el pedido de prueba'),
               ('mail.mail_activity_data_meeting', 'Reunión de seguimiento con el cliente'),
               ('mail.mail_activity_data_email', 'Enviar cotización actualizada'),
               ('mail.mail_activity_data_todo', 'Coordinar muestras de producto')],
    'vencida': [('mail.mail_activity_data_call', 'Llamar al cliente: sin respuesta desde la visita'),
                ('mail.mail_activity_data_email', 'Responder la contrapropuesta de precios'),
                ('mail.mail_activity_data_todo', 'Revisar la línea de crédito del cliente')],
}
NOTAS = [
    'El cliente compara con otro proveedor y pide un plazo de entrega más corto.',
    'Interesado en los helados de paleta y el panetón de 900 g; pide precios por caja.',
    'Quiere probar con un pedido pequeño antes de comprometer volumen.',
    'Pide factura con RUC y entrega en su almacén; se coordina con el CD Arequipa.',
    'Confirma que recibe la mercadería los martes y jueves por la mañana.',
    'El dueño viaja la próxima semana; se retoma el contacto a su regreso.',
]


def _fechar_lead(env, lead, desde, cuando):
    fechar_mensajes(env, 'crm.lead', lead.id, desde, cuando)


def cargar_crm(env):
    rng = random.Random(SEMILLA + 11)
    Lead = env['crm.lead'].with_context(active_test=False, mail_activity_quick_update=True)
    Partner = env['res.partner']
    motivos = []
    for nombre in MOTIVOS_PERDIDA:
        motivo = env['crm.lost.reason'].search([('name', '=', nombre)], limit=1) or env['crm.lost.reason'].create({'name': nombre})
        motivos.append(motivo)
    etapas = {k: ref(env, v) for k, v in ETAPA.items()}
    todas = dict(OPORTUNIDADES, **OPORTUNIDADES_NUEVAS)
    ganadas = perdidas = abiertas = 0
    for nombre, d in todas.items():
        cliente = Partner.search([('name', '=', d['cliente'])], limit=1)
        assert cliente, f'No existe el cliente {d["cliente"]}'
        lead = Lead.search([('name', '=', nombre), ('type', '=', 'opportunity')], limit=1)
        vendedor = usuario(env, d.get('vendedor', 'user_jefe_ventas')) if not lead else lead.user_id
        mid = ultimo_mensaje(env)
        if not lead:
            lead = Lead.with_user(vendedor).create({
                'name': nombre, 'type': 'opportunity', 'partner_id': cliente.id, 'user_id': vendedor.id,
                'team_id': ref(env, d['equipo']).id, 'stage_id': etapas['prospecto'].id,
                'expected_revenue': d['ingreso'], 'probability': PROBABILIDAD['prospecto']})
        lead = lead.with_user(vendedor)
        lead.write({'partner_id': cliente.id, 'priority': d['prioridad'], 'stage_id': etapas['prospecto'].id,
                    'probability': PROBABILIDAD['prospecto'], 'date_deadline': d.get('esperado') or d.get('cierre')})
        alta = lima(d['alta'], rng.randint(9, 16), rng.randint(0, 59))
        _fechar_lead(env, lead, mid, alta)
        env.cr.execute("UPDATE crm_lead SET create_date = %s, write_date = %s, date_open = %s, date_last_stage_update = %s, date_closed = NULL WHERE id = %s",
                       (alta, alta, alta, alta, lead.id))
        # Línea de tiempo: cada etapa trae su actividad hecha y a veces una nota
        pasos = list(d['etapas'])
        for orden, (etapa, dia) in enumerate([('prospecto', d['alta'])] + pasos):
            momento_ = lima(dia, rng.randint(9, 17), rng.randint(0, 59))
            if etapa != 'prospecto':
                mid = ultimo_mensaje(env)
                lead.write({'stage_id': etapas[etapa].id, 'probability': PROBABILIDAD[etapa]})
                _fechar_lead(env, lead, mid, momento_)
                env.cr.execute("UPDATE crm_lead SET date_last_stage_update = %s WHERE id = %s", (momento_, lead.id))
            if etapa == 'prospecto':
                continue
            tipo, resumen, feedback = rng.choice(ACTIVIDADES_HECHAS[etapa])
            actividad = lead.activity_schedule(tipo, date_deadline=dia, summary=resumen, user_id=vendedor.id)
            env.cr.execute("UPDATE mail_activity SET create_date = %s WHERE id = %s", (momento_ - timedelta(days=2), actividad.id))
            mid = ultimo_mensaje(env)
            actividad.with_user(vendedor).action_feedback(feedback=feedback)
            _fechar_lead(env, lead, mid, momento_ + timedelta(minutes=20))
            if rng.random() < 0.6:
                mid = ultimo_mensaje(env)
                lead.message_post(body=rng.choice(NOTAS), message_type='comment', subtype_xmlid='mail.mt_note')
                _fechar_lead(env, lead, mid, momento_ + timedelta(hours=1))
        # Cierre
        if d['final'] == 'ganada':
            cierre = lima(d['cierre'], rng.randint(10, 17), rng.randint(0, 59))
            mid = ultimo_mensaje(env)
            lead.action_set_won()
            _fechar_lead(env, lead, mid, cierre)
            lead.message_post(body='Ganada: el cliente confirmó su primer pedido.', message_type='comment',
                              subtype_xmlid='mail.mt_note')
            _fechar_lead(env, lead, mid, cierre)
            env.cr.execute("UPDATE crm_lead SET date_closed = %s, date_last_stage_update = %s, date_deadline = %s WHERE id = %s",
                           (cierre, cierre, d['cierre'], lead.id))
            vincular_pedido(env, lead, cliente, d['cierre'])
            ganadas += 1
        elif d['final'] == 'perdida':
            cierre = lima(d['cierre'], rng.randint(10, 17), rng.randint(0, 59))
            mid = ultimo_mensaje(env)
            lead.action_set_lost(lost_reason_id=motivos[d['motivo']].id)
            _fechar_lead(env, lead, mid, cierre)
            env.cr.execute("UPDATE crm_lead SET date_closed = %s, date_deadline = %s WHERE id = %s",
                           (cierre, d['cierre'], lead.id))
            perdidas += 1
        else:
            tipo, resumen = rng.choice(ACTIVIDADES_PENDIENTES[d['pendiente']])
            if d['pendiente'] == 'vencida':
                plazo = HOY - timedelta(days=rng.randint(2, 9))
            else:
                plazo = HOY + timedelta(days=rng.randint(1, 12))
            actividad = lead.activity_schedule(tipo, date_deadline=plazo, summary=resumen, user_id=vendedor.id)
            env.cr.execute("UPDATE mail_activity SET create_date = %s WHERE id = %s",
                           (lima(min(plazo - timedelta(days=4), FIN)), actividad.id))
            if rng.random() < 0.5:     # una segunda actividad, para ver el chatter con varias a la vez
                otra = lead.activity_schedule('mail.mail_activity_data_todo', date_deadline=HOY + timedelta(days=rng.randint(3, 15)),
                                              summary='Preparar contrato de suministro', user_id=vendedor.id)
                env.cr.execute("UPDATE mail_activity SET create_date = %s WHERE id = %s", (lima(FIN), otra.id))
            abiertas += 1
        env.flush_all()
        env.cr.execute("""UPDATE crm_lead SET date_open = create_date, day_open = 0,
                                              day_close = CASE WHEN date_closed IS NOT NULL
                                                               THEN GREATEST(EXTRACT(EPOCH FROM (date_closed - create_date)) / 86400, 0) END
                          WHERE id = %s""", (lead.id,))
    env.invalidate_all()
    print(f'  CRM: {len(todas)} oportunidades enlazadas a clientes: {ganadas} ganadas, {perdidas} perdidas, {abiertas} abiertas.')


def vincular_pedido(env, lead, cliente, cierre):
    """La oportunidad ganada queda ligada al primer pedido del cliente a partir de su cierre (o al último, si no hay)."""
    Pedido = env['sale.order'].sudo()
    pedido = Pedido.search([('partner_id', '=', cliente.id), ('state', '=', 'sale'), ('date_order', '>=', lima(cierre, 0)),
                            ('opportunity_id', '=', False)], order='date_order', limit=1)
    if not pedido:
        pedido = Pedido.search([('partner_id', '=', cliente.id), ('state', '=', 'sale'), ('opportunity_id', '=', False)],
                               order='date_order desc', limit=1)
    if pedido:
        pedido.opportunity_id = lead.id


# --- Calidad ------------------------------------------------------------------------------------------------

MOTIVOS_RECHAZO = [
    'Peso neto fuera de tolerancia: unidades por debajo del 98 % del peso nominal.',
    'Análisis microbiológico: recuento de coliformes sobre el límite permitido.',
    'Humedad del panetón fuera de rango: masa demasiado seca.',
    'Endurecimiento incompleto: el producto salió del túnel por encima de −18 °C.',
    'Pasteurización fuera de rango: la mezcla no alcanzó la temperatura mínima.',
]
RECHAZOS = 9
OBSERVADAS = 3          # en medición con un punto que no cumple, a la espera de decisión
EN_MEDICION_RECIENTES = 3
PENDIENTES_RECIENTES = 4


def medida_que_cumple(rng, punto):
    amplitud = punto.valor_max - punto.valor_min
    return round(rng.uniform(punto.valor_min + amplitud * 0.15, punto.valor_max - amplitud * 0.15), 3)


def medida_fuera(rng, punto):
    amplitud = punto.valor_max - punto.valor_min
    return round(punto.valor_min - amplitud * rng.uniform(0.05, 0.2) if rng.random() < 0.5
                 else punto.valor_max + amplitud * rng.uniform(0.05, 0.2), 3)


def medir(rng, inspeccion, falla=None, hasta=None):
    """Mide los puntos de la inspección; ``falla`` es el nombre del punto que no cumple; ``hasta`` mide solo los primeros."""
    lineas = inspeccion.linea_ids.sorted('sequence')
    if hasta is not None:
        lineas = lineas[:hasta]
    for linea in lineas:
        punto = linea.punto_id
        if punto.tipo == 'aprobacion':
            linea.write({'cumple_manual': falla != punto.name})
        else:
            linea.write({'medicion': medida_fuera(rng, punto) if falla == punto.name else medida_que_cumple(rng, punto)})


def cargar_calidad(env):
    rng = random.Random(SEMILLA + 12)
    Inspeccion = env['donofrio.calidad.inspeccion']
    inspector = usuario(env, 'user_inspector_calidad')
    jefe_produccion = usuario(env, 'user_jefe_produccion')
    ordenes = env['mrp.production'].search([('state', '=', 'done')], order='date_start, id')
    # Las órdenes terminadas tienen como fecha de fin la de la corrida (25/11); se corrige con la última operación
    # de cada una (la fecha de inicio ya es la histórica)
    env.cr.execute("""UPDATE mrp_production p SET date_finished = w.fin
                        FROM (SELECT production_id, MAX(date_finished) AS fin FROM mrp_workorder
                               WHERE date_finished IS NOT NULL GROUP BY production_id) w
                       WHERE w.production_id = p.id AND p.state = 'done' AND p.date_finished > %s""", (lima(FIN, 23),))
    env.cr.execute("""UPDATE mrp_production SET date_finished = date_start + interval '5 hours'
                       WHERE state = 'done' AND date_finished > %s""", (lima(FIN, 23),))
    env.invalidate_all()
    # El responsable de cada orden es el jefe de producción (antes quedaba el usuario técnico)
    ordenes.with_context(tracking_disable=True).write({'user_id': jefe_produccion.id})
    mid_inicial = ultimo_mensaje(env)
    ordenes._crear_inspecciones()                 # el mismo método que usa el módulo al terminar cada orden
    inspecciones = Inspeccion.search([('production_id', 'in', ordenes.ids), ('state', '=', 'borrador')],
                                     order='id').sorted(lambda i: (i.production_id.date_start, i.id))
    total = len(inspecciones)
    pendientes = inspecciones[-PENDIENTES_RECIENTES:]       # las más nuevas siguen pendientes
    en_medicion = inspecciones[-(PENDIENTES_RECIENTES + EN_MEDICION_RECIENTES):-PENDIENTES_RECIENTES]
    resto = inspecciones[:total - PENDIENTES_RECIENTES - EN_MEDICION_RECIENTES]
    # Rechazos: sobre todo en lotes de las últimas semanas (aún tienen stock), alguno más antiguo
    con_stock = resto.filtered(lambda i: i.lot_id.product_qty > 0)
    recientes_con_stock = con_stock[-30:]
    rechazadas = rng.sample(list(recientes_con_stock), min(RECHAZOS - 2, len(recientes_con_stock)))
    rechazadas += rng.sample([i for i in resto[:60] if i not in rechazadas], 2)
    candidatas = [i for i in resto if i not in rechazadas]
    observadas = rng.sample(candidatas[-40:], OBSERVADAS)
    rechazadas_set, observadas_set, pendientes_set, medicion_set = set(rechazadas), set(observadas), set(pendientes), set(en_medicion)
    contador = {'aprobada': 0, 'rechazada': 0, 'en_curso': 0, 'borrador': 0}
    for inspeccion in inspecciones:
        orden = inspeccion.production_id
        fin = orden.date_finished
        inicio = fin + timedelta(hours=rng.randint(18, 26))
        if inicio.date() > FIN:
            inicio = datetime.combine(FIN, time(15, 0)) + timedelta(minutes=rng.randint(0, 120))
        mid = mid_inicial
        ins = inspeccion.with_user(inspector).with_context(mail_activity_quick_update=True)   # sin correos de aviso
        if inspeccion in pendientes_set:
            contador['borrador'] += 1
        else:
            ins.action_iniciar()
            categoria = inspeccion.product_id.categ_id.complete_name or ''
            puntos = ins.linea_ids.punto_id.filtered(lambda p: p.tipo == 'rango')
            if inspeccion in medicion_set:
                medir(rng, ins, hasta=rng.randint(1, max(1, len(ins.linea_ids) - 1)))
                contador['en_curso'] += 1
            elif inspeccion in observadas_set:
                punto = rng.choice(puntos.filtered(lambda p: 'Peso' in p.name) or puntos)
                medir(rng, ins, falla=punto.name)
                contador['en_curso'] += 1
            elif inspeccion in rechazadas_set:
                micro = ins.linea_ids.punto_id.filtered(lambda p: p.tipo == 'aprobacion')
                falla = micro[:1].name if rng.random() < 0.35 and micro else rng.choice(puntos).name
                medir(rng, ins, falla=falla)
                motivo = next((m for m in MOTIVOS_RECHAZO if falla.split()[0].lower()[:6] in m.lower()), rng.choice(MOTIVOS_RECHAZO))
                ins.write({'motivo_rechazo': motivo})
                ins.action_rechazar()
                contador['rechazada'] += 1
            else:
                medir(rng, ins)
                ins.action_aprobar()
                contador['aprobada'] += 1
        fechar_mensajes(env, 'donofrio.calidad.inspeccion', inspeccion.id, mid, inicio)
        env.cr.execute("""UPDATE mail_message SET date = %s, create_date = %s
                           WHERE id = (SELECT MIN(id) FROM mail_message WHERE model = %s AND res_id = %s)""",
                       (fin + timedelta(minutes=5), fin + timedelta(minutes=5), 'donofrio.calidad.inspeccion', inspeccion.id))
        fechar_mensajes(env, 'mrp.production', orden.id, mid, inicio + timedelta(hours=1))
        env.cr.execute("UPDATE donofrio_calidad_inspeccion SET create_date = %s, write_date = %s WHERE id = %s",
                       (fin + timedelta(minutes=5), inicio + timedelta(hours=1), inspeccion.id))
        # La actividad de decidir el destino del lote rechazado nace el día del rechazo
        env.cr.execute("""UPDATE mail_activity SET create_date = %s, date_deadline = %s
                           WHERE res_model = 'mrp.production' AND res_id = %s AND summary LIKE %s""",
                       (inicio, inicio.date() + timedelta(days=2), orden.id, f'%{inspeccion.lot_id.name}%'))
        if inspeccion in rechazadas_set and (HOY - inicio.date()).days > 12:
            # Lo antiguo ya se resolvió: se cierra la actividad de decidir el destino del lote, dos días después
            mid = ultimo_mensaje(env)
            for actividad in orden.activity_ids.filtered(lambda a: a.summary and inspeccion.lot_id.name in a.summary):
                actividad.with_user(jefe_produccion).action_feedback(
                    feedback=rng.choice(['Lote reprocesado y vuelto a inspeccionar.', 'Lote descartado y registrado como merma.']))
            fechar_mensajes(env, 'mrp.production', orden.id, mid, inicio + timedelta(days=2, hours=3))
    env.invalidate_all()
    print(f'  Calidad: {total} inspecciones: {contador["aprobada"]} aprobadas, {contador["rechazada"]} rechazadas, '
          f'{contador["en_curso"]} en medición (observadas o recientes), {contador["borrador"]} pendientes.')


# --- Heladeros ----------------------------------------------------------------------------------------------

def efectivo_con_diferencia(rng, importe):
    """Casi siempre cuadra; a veces el heladero entrega unos soles de menos (o de más)."""
    suerte = rng.random()
    if suerte < 0.78:
        return round(importe, 2)
    diferencia = rng.choice([-0.5, -1.0, -1.5, -2.0, -3.0, 0.5, 1.0])
    return round(importe + diferencia, 2)


def cargar_heladeros(env):
    rng = random.Random(SEMILLA + 13)
    liquidador = usuario(env, 'user_liquidador')
    Liquidacion = env['donofrio.liquidacion'].with_user(liquidador).with_context(mail_notrack=False)
    pedidos = env['sale.order'].search([('team_id', '=', ref(env, 'equipo_heladeros').id), ('state', '=', 'sale'),
                                        ('partner_id.category_id', 'in', ref(env, 'cat_heladero').ids)],
                                       order='date_order, id')
    lista = ref(env, 'lista_heladero')
    cantidad = merma_total = 0
    importe_total = 0.0
    for pedido in pedidos:
        dia = (pedido.date_order - DESFASE_LIMA).date()
        if Liquidacion.sudo().search_count([('partner_id', '=', pedido.partner_id.id), ('fecha', '=', dia)]):
            continue
        vendidas = {}
        for linea in pedido.order_line.filtered(lambda lin: not lin.display_type):
            vendidas[linea.product_id] = vendidas.get(linea.product_id, 0.0) + linea.product_uom_qty
        lineas = []
        for producto, vendido in vendidas.items():
            devuelto = 0 if rng.random() < 0.6 else rng.randint(1, max(1, round(vendido * 0.03)))
            merma = 0 if rng.random() < 0.7 else rng.randint(1, max(1, round(vendido * 0.015)))
            lineas.append(Command.create({'product_id': producto.id, 'despachado': vendido + devuelto + merma,
                                          'devuelto': devuelto, 'merma': merma}))
            merma_total += merma
        mid = ultimo_mensaje(env)
        liquidacion = Liquidacion.create({
            'partner_id': pedido.partner_id.id, 'fecha': dia, 'pricelist_id': lista.id, 'linea_ids': lineas,
            'liquidador_id': liquidador.id})
        liquidacion.action_despachar()
        liquidacion.efectivo_entregado = efectivo_con_diferencia(rng, liquidacion.total_importe)
        # Se liquida contra el pedido que ya existe (action_confirmar crearía uno nuevo y duplicaría la venta)
        liquidacion.sudo().write({'state': 'liquidado', 'order_id': pedido.id})
        pedido.sudo().write({'origin': liquidacion.name})
        cierre = lima(dia, 19, rng.randint(0, 59))
        fechar_mensajes(env, 'donofrio.liquidacion', liquidacion.id, mid, cierre)
        env.cr.execute("UPDATE donofrio_liquidacion SET create_date = %s, write_date = %s WHERE id = %s",
                       (lima(dia, 7, rng.randint(0, 40)), cierre, liquidacion.id))
        cantidad += 1
        importe_total += liquidacion.total_importe
    # Las del último día (domingo 22/11) siguen sin liquidar: dos despachadas y una en borrador
    heladeros = env['res.partner'].search([('category_id', 'in', ref(env, 'cat_heladero').ids)], order='id')
    productos = env['product.product'].search([('default_code', 'in', ['PT-H01', 'PT-H03', 'PT-H05', 'PT-H07', 'PT-H10'])])
    pendientes = 0
    for indice, heladero in enumerate(heladeros[:3]):
        if Liquidacion.sudo().search_count([('partner_id', '=', heladero.id), ('fecha', '=', FIN)]):
            continue
        mid = ultimo_mensaje(env)
        liquidacion = Liquidacion.create({
            'partner_id': heladero.id, 'fecha': FIN, 'pricelist_id': lista.id, 'liquidador_id': liquidador.id,
            'linea_ids': [Command.create({'product_id': p.id, 'despachado': rng.choice([60, 80, 100, 120])})
                          for p in productos[:rng.randint(3, 5)]]})
        if indice < 2:
            liquidacion.action_despachar()
        fechar_mensajes(env, 'donofrio.liquidacion', liquidacion.id, mid, lima(FIN, 7, 30 + indice))
        env.cr.execute("UPDATE donofrio_liquidacion SET create_date = %s, write_date = %s WHERE id = %s",
                       (lima(FIN, 7, 30 + indice), lima(FIN, 7, 45 + indice), liquidacion.id))
        pendientes += 1
    env.invalidate_all()
    print(f'  Heladeros: {cantidad} liquidaciones cuadradas con sus pedidos (S/ {importe_total:,.2f} en total, '
          f'{merma_total:.0f} unidades de merma) y {pendientes} pendientes del último día.')


# --- Cadena de frío -----------------------------------------------------------------------------------------

# xmlid de la cámara → (temperatura media, desvío); los rangos de control están en el módulo (−30 a −18 y 2 a 6)
CAMARAS = {
    'loc_lim_congelacion': (-24.0, 1.1), 'loc_aqp_congelacion': (-23.5, 1.3),
    'loc_lim_refrigerados': (4.0, 0.55), 'loc_aqp_refrigerada': (4.2, 0.6),
}
# Incidentes: (cámara, día, hora de Lima, lectura, observación, lectura de recuperación)
INCIDENTES = [
    ('loc_lim_congelacion', date(2026, 8, 19), 7, -15.8, 'Corte de energía durante la madrugada; el grupo electrógeno tardó en arrancar.', -21.4),
    ('loc_aqp_congelacion', date(2026, 9, 11), 15, -16.4, 'Puerta abierta durante la carga de los triciclos.', -22.9),
    ('loc_lim_refrigerados', date(2026, 10, 6), 7, 7.9, 'Compresor con falla; se llamó al técnico.', 4.6),
    ('loc_aqp_refrigerada', date(2026, 10, 28), 15, 6.8, 'Puerta mal cerrada después del ingreso de insumos.', 4.1),
    ('loc_lim_congelacion', date(2026, 11, 10), 7, -16.9, 'Escarcha en el evaporador; se programó el deshielo.', -22.0),
    ('loc_aqp_congelacion', date(2026, 11, 19), 15, -14.7, 'Falla del termostato; se movió el producto a la otra cámara.', -20.8),
    ('loc_lim_refrigerados', date(2026, 11, 21), 7, 7.3, 'Descarga de insumos con la puerta abierta más de 20 minutos.', 4.8),
]


def cargar_frio(env):
    rng = random.Random(SEMILLA + 14)
    jefe = usuario(env, 'user_jefe_almacen')
    Temperatura = env['donofrio.temperatura'].sudo().with_context(tracking_disable=True, mail_create_nolog=True,
                                                                  mail_activity_quick_update=True)
    incidentes = {(c, d, h): (valor, texto, recupera) for c, d, h, valor, texto, recupera in INCIDENTES}
    valores, lecturas = [], 0
    for xmlid, (media, desvio) in CAMARAS.items():
        ubicacion = ref(env, xmlid)
        dia = INICIO
        while dia <= FIN:
            for hora in (7, 15):
                incidente = incidentes.get((xmlid, dia, hora))
                recuperacion = incidentes.get((xmlid, dia, hora - 8))
                observacion = False
                if incidente:
                    temperatura, observacion, _ = incidente
                elif recuperacion:
                    temperatura, observacion = recuperacion[2], 'Temperatura recuperada después de atender el incidente de la mañana.'
                else:
                    temperatura = round(max(ubicacion.temp_min + 1.2, min(ubicacion.temp_max - 0.9, rng.gauss(media, desvio))), 1)
                valores.append({'location_id': ubicacion.id, 'temperatura': temperatura, 'user_id': jefe.id,
                                'fecha': lima(dia, hora, rng.randint(0, 25)), 'observaciones': observacion})
            dia += timedelta(days=1)
    lecturas_creadas = Temperatura.create(valores)       # las fuera de rango generan su actividad (_alertar)
    lecturas = len(lecturas_creadas)
    fuera = lecturas_creadas.filtered('fuera_de_rango')
    for lectura in fuera:
        env.cr.execute("UPDATE mail_activity SET create_date = %s, date_deadline = %s WHERE res_model = 'donofrio.temperatura' AND res_id = %s",
                       (lectura.fecha, lectura.fecha.date() + timedelta(days=1), lectura.id))
        if (HOY - lectura.fecha.date()).days > 7:      # lo antiguo ya se atendió; las últimas siguen pendientes
            mid = ultimo_mensaje(env)
            for actividad in lectura.activity_ids:
                actividad.with_user(jefe).action_feedback(
                    feedback='Se revisó la cámara y los lotes almacenados; producto conservado, sin pérdida.')
            fechar_mensajes(env, 'donofrio.temperatura', lectura.id, mid, lectura.fecha + timedelta(hours=3))
    env.invalidate_all()
    print(f'  Frío: {lecturas} lecturas en {len(CAMARAS)} cámaras, {len(fuera)} fuera de rango con su alerta.')


# --- Mesa de servicios --------------------------------------------------------------------------------------

# (título, tipo, prioridad, etapa final, alta, horas de resolución respecto de la fecha límite (<0 antes, >0 tarde), solicitante, descripción)
TICKETS = [
    ('No puedo entrar al ERP: usuario bloqueado', 'solicitud_acceso', '2', 'cerrado', (date(2026, 8, 6), 9), -3, 'user_vendedor',
     'Después de tres intentos fallidos el usuario quedó bloqueado. Se desbloqueó y se pidió cambiar la contraseña.'),
    ('Alta de usuario para el nuevo cajero del turno tarde', 'solicitud_acceso', '1', 'cerrado', (date(2026, 8, 10), 10), -20, 'user_jefe_ventas',
     'Se creó el usuario con el rol de cajero del PdV y se entregó la contraseña inicial por el canal acordado.'),
    ('Lentitud al cargar el inventario en Arequipa', 'incidente', '2', 'cerrado', (date(2026, 8, 24), 8), -2, 'user_jefe_almacen',
     'La vista de existencias tardaba más de 20 segundos. Se agregó un filtro por almacén y mejoró.'),
    ('Impresora de etiquetas de lotes sin conexión (planta Lima)', 'incidente', '3', 'cerrado', (date(2026, 9, 2), 7), -1, 'user_jefe_produccion',
     'La impresora perdió la red. Se reinició y se fijó su dirección IP.'),
    ('Cambiar el rango de temperatura de la cámara refrigerada', 'solicitud_servicio', '0', 'cerrado', (date(2026, 9, 14), 11), -30, 'user_jefe_almacen',
     'Se confirmó el rango de 2 a 6 °C con el jefe de almacén; no hizo falta cambiarlo.'),
    ('Error al confirmar un pedido con la lista Verano', 'incidente', '2', 'cerrado', (date(2026, 9, 21), 15), 6, 'user_jefe_ventas',
     'El pedido no confirmaba por una regla de precios vencida. Se corrigió la vigencia de la regla.'),
    ('Reporte de mermas por heladero', 'solicitud_servicio', '1', 'cerrado', (date(2026, 9, 30), 9), -12, 'user_liquidador',
     'Se armó una vista agrupada de las liquidaciones por heladero y mes, con la merma y la diferencia de efectivo.'),
    ('Acceso de solo lectura al tablero para el contador', 'solicitud_acceso', '0', 'cerrado', (date(2026, 10, 8), 9), -50, 'user_contador',
     'Se dio acceso de lectura al tablero gerencial al contador, con aprobación de la gerencia.'),
    ('La balanza no envía el peso al registro de producción', 'incidente', '3', 'resuelto', (date(2026, 10, 19), 6), 2, 'user_jefe_produccion',
     'El cable de la balanza estaba suelto. Se cambió y se probó con tres lotes; se espera la confirmación del jefe de producción.'),
    ('El respaldo diario falló esta madrugada', 'incidente', '3', 'cerrado', (date(2026, 10, 27), 6), -2, 'admin',
     'El disco de respaldos estaba lleno. Se liberó espacio y se verificó la restauración con el último respaldo.'),
    ('Actualizar la lista de precios Campaña Navidad', 'solicitud_servicio', '1', 'cerrado', (date(2026, 11, 2), 10), -8, 'user_jefe_ventas',
     'Se cargó la nueva regla del panetón de 900 g con vigencia del 1/10 al 31/12.'),
    ('El cierre de caja del PdV no cuadra el domingo', 'incidente', '2', 'resuelto', (date(2026, 11, 9), 14), -1, 'user_cajero_pdv',
     'La diferencia venía de un pago con Yape registrado como efectivo. Se corrigió el método de pago.'),
    ('Nuevo usuario inspector de calidad para el turno noche', 'solicitud_acceso', '1', 'atencion', (date(2026, 11, 16), 9), None, 'user_jefe_produccion',
     'Se pide un usuario con el rol de inspector de calidad. Pendiente la aprobación del jefe de producción.'),
    ('Las etiquetas del certificado de calidad salen cortadas', 'incidente', '1', 'analisis', (date(2026, 11, 18), 10), None, 'user_inspector_calidad',
     'Al imprimir el certificado, el nombre del producto se corta en el borde derecho de la hoja.'),
    ('Exportar las liquidaciones de heladeros a Excel', 'solicitud_servicio', '0', 'nuevo', (date(2026, 11, 20), 16), None, 'user_liquidador',
     'El liquidador pide una exportación mensual de las liquidaciones para enviarla a contabilidad.'),
    ('No llegan los correos de alerta de temperatura', 'incidente', '2', 'analisis', (date(2026, 11, 21), 8), None, 'user_jefe_almacen',
     'El jefe de almacén ve la actividad en el sistema, pero no le llega el correo de aviso.'),
    ('Duplicado: el tablero tarda en abrir', 'incidente', '1', 'cancelado', (date(2026, 11, 12), 9), None, 'user_gerente',
     'Es el mismo caso de «Tablero gerencial no carga», ya cerrado; se cancela por duplicado.'),
]
ETAPAS_MESA = ['nuevo', 'analisis', 'atencion', 'resuelto', 'cerrado']
TIPOS_MESA = {'incidente': 'etiqueta_ti_incidente', 'solicitud_servicio': 'etiqueta_ti_solicitud_servicio',
              'solicitud_acceso': 'etiqueta_ti_solicitud_acceso'}
HORAS_SLA = {'3': 4, '2': 8, '1': 72, '0': 120}


def cargar_mesa(env):
    rng = random.Random(SEMILLA + 15)
    admin = env.ref('base.user_admin')
    mesa = ref(env, 'proyecto_mesa_servicios')
    Tarea = env['project.task'].with_user(admin).with_context(mail_activity_quick_update=True)
    etapa = {k: ref(env, f'etapa_ti_{k}') for k in ('nuevo', 'analisis', 'atencion', 'resuelto', 'cerrado')}
    etapa['cancelado'] = etapa['cerrado']
    # Los cinco tickets que ya trae donofrio_base se fechan dentro del periodo (los dos cerrados con su historia)
    for xmlid, alta in (('ticket_ti_tablero', (date(2026, 11, 20), 12)), ('ticket_ti_acceso_liquidador', (date(2026, 11, 16), 15))):
        ticket = ref(env, xmlid)
        momento_ = lima(*alta)
        env.cr.execute("UPDATE project_task SET create_date = %s, date_last_stage_update = %s WHERE id = %s", (momento_, ticket.date_end or momento_, ticket.id))
        fechar_mensajes(env, 'project.task', ticket.id, 0, momento_)
    creados = cerrados = 0
    estados = {'cerrado': '1_done', 'resuelto': '1_done', 'cancelado': '1_canceled'}
    for titulo, tipo, prioridad, final, (dia, hora), desvio, solicitante, descripcion in TICKETS:
        alta = lima(dia, hora, rng.randint(0, 40))
        limite = alta + timedelta(hours=HORAS_SLA[prioridad])
        solicitante_ = usuario(env, solicitante)
        mid = ultimo_mensaje(env)
        ticket = Tarea.create({
            'name': titulo, 'project_id': mesa.id, 'stage_id': etapa['nuevo'].id, 'priority': prioridad,
            'tag_ids': [Command.set([ref(env, TIPOS_MESA[tipo]).id])], 'user_ids': [Command.set([admin.id])],
            'partner_id': solicitante_.partner_id.id, 'date_deadline': limite, 'description': f'<p>{descripcion}</p>'})
        env.cr.execute("UPDATE project_task SET create_date = %s, write_date = %s, date_assign = %s, date_last_stage_update = %s WHERE id = %s",
                       (alta, alta, alta, alta, ticket.id))
        fechar_mensajes(env, 'project.task', ticket.id, mid, alta)
        # Avanza por las etapas hasta la final, con su fecha
        indice_final = ETAPAS_MESA.index('cerrado' if final == 'cancelado' else final)
        momento_ = alta
        for nombre in ETAPAS_MESA[1:indice_final + 1]:
            momento_ += timedelta(hours=rng.randint(1, 6)) if nombre != 'cerrado' else timedelta(hours=1)
            mid = ultimo_mensaje(env)
            ticket.write({'stage_id': etapa[nombre].id})
            fechar_mensajes(env, 'project.task', ticket.id, mid, momento_)
            env.cr.execute("UPDATE project_task SET date_last_stage_update = %s WHERE id = %s", (momento_, ticket.id))
        if final in estados:
            if final == 'cancelado':
                cierre = alta + timedelta(hours=rng.randint(2, 20))
            else:
                cierre = limite + timedelta(hours=desvio)
            mid = ultimo_mensaje(env)
            ticket.write({'state': estados[final]})
            ticket.write({'date_end': cierre})          # aparte: Odoo pisa la fecha de cierre si se escribe junto con la etapa
            ticket.message_post(body=f'Atendido: {descripcion}', message_type='comment', subtype_xmlid='mail.mt_note')
            fechar_mensajes(env, 'project.task', ticket.id, mid, cierre)
            env.cr.execute("UPDATE project_task SET date_last_stage_update = %s WHERE id = %s", (cierre, ticket.id))
            cerrados += 1
        else:
            nota_en = min(alta + timedelta(hours=rng.randint(2, 20)), lima(FIN, 20))
            mid = ultimo_mensaje(env)
            ticket.message_post(body='Se recibió el ticket y se está atendiendo.', message_type='comment', subtype_xmlid='mail.mt_note')
            fechar_mensajes(env, 'project.task', ticket.id, mid, nota_en)
        creados += 1
    env.invalidate_all()
    print(f'  Mesa de servicios: {creados} tickets nuevos ({cerrados} cerrados o resueltos) más los 5 que ya había.')


# --- Calendario ---------------------------------------------------------------------------------------------

def crear_evento(env, nombre, dia, hora, minutos, organizador, asistentes, lugar=False, descripcion=False,
                 lead=None, pasado=True, **extra):
    """Crea la reunión sin avisar por correo y deja a los asistentes con la invitación aceptada."""
    Evento = env['calendar.event'].with_context(no_mail_to_attendees=True, dont_notify=True, mail_notrack=True,
                                                mail_create_nolog=True)
    valores = {
        'name': nombre, 'start': lima(dia, hora[0], hora[1]), 'stop': lima(dia, hora[0], hora[1]) + timedelta(minutes=minutos),
        'user_id': organizador.id, 'partner_ids': [Command.set([organizador.partner_id.id] + [a.id for a in asistentes])],
        'location': lugar, 'description': f'<p>{descripcion}</p>' if descripcion else False, 'event_tz': 'America/Lima'}
    if lead:
        valores['opportunity_id'] = lead.id
    valores.update(extra)
    mid = ultimo_mensaje(env)
    evento = Evento.create(valores)
    if pasado:
        evento.attendee_ids.write({'state': 'accepted'})
    if lead:
        fechar_mensajes(env, 'crm.lead', lead.id, mid, lima(dia, hora[0], hora[1]) - timedelta(days=1))
    return evento


def cargar_calendario(env):
    rng = random.Random(SEMILLA + 16)
    u = lambda x: usuario(env, x)    # noqa: E731
    produccion, almacen, calidad, ventas, gerente = u('user_jefe_produccion'), u('user_jefe_almacen'), u('user_inspector_calidad'), u('user_jefe_ventas'), u('user_gerente')
    contador, liquidador, vendedor, compras = u('user_contador'), u('user_liquidador'), u('user_vendedor'), u('user_compras')
    Evento = env['calendar.event'].with_context(no_mail_to_attendees=True, dont_notify=True, mail_notrack=True, mail_create_nolog=True)
    n = 0
    # Reunión semanal de producción y calidad: martes 8:30 (16 martes, del 4/8 al 17/11)
    semanal = Evento.create({
        'name': 'Reunión semanal de producción y calidad', 'start': lima(date(2026, 8, 4), 8, 30), 'stop': lima(date(2026, 8, 4), 9, 30),
        'user_id': produccion.id, 'location': 'Sala de reuniones, Planta Lima', 'event_tz': 'America/Lima',
        'partner_ids': [Command.set([x.partner_id.id for x in (produccion, almacen, calidad, ventas)])],
        'description': '<p>Plan de producción de la semana, lotes en medición y alertas de la cadena de frío.</p>',
        'recurrency': True, 'rrule_type': 'weekly', 'tue': True, 'interval': 1, 'end_type': 'count', 'count': 16})
    n += len(semanal.recurrence_id.calendar_event_ids)
    # Comité de gerencia: primer lunes de cada mes
    comite = Evento.create({
        'name': 'Comité de gerencia: cierre y metas del mes', 'start': lima(date(2026, 8, 3), 10, 0), 'stop': lima(date(2026, 8, 3), 11, 30),
        'user_id': gerente.id, 'location': 'Oficina de gerencia, Lima', 'event_tz': 'America/Lima',
        'partner_ids': [Command.set([x.partner_id.id for x in (gerente, ventas, produccion, almacen, contador)])],
        'description': '<p>Ventas y producción del mes anterior, existencias por vencer y metas del mes.</p>',
        'recurrency': True, 'rrule_type': 'monthly', 'month_by': 'day', 'byday': '1', 'weekday': 'MON', 'end_type': 'count', 'count': 4})
    n += len(comite.recurrence_id.calendar_event_ids)
    for evento in (semanal.recurrence_id.calendar_event_ids | comite.recurrence_id.calendar_event_ids):
        evento.attendee_ids.write({'state': 'accepted'})
    # Reuniones sueltas
    sueltas = [
        ('Capacitación de heladeros: temporada de verano', date(2026, 9, 14), (9, 0), 180, liquidador,
         [vendedor] + list(env['res.partner'].search([('category_id', 'in', ref(env, 'cat_heladero').ids)], limit=8)),
         'CD Arequipa, sala de capacitación', 'Higiene, manejo de la cadena de frío en el triciclo y cierre de la liquidación diaria.'),
        ('Lanzamiento de la campaña de panetón', date(2026, 10, 5), (15, 0), 90, ventas, [gerente, produccion, vendedor],
         'Sala de reuniones, Planta Lima', 'Metas por canal, lista «Campaña Navidad» y plan de producción de octubre a diciembre.'),
        ('Auditoría interna HACCP / ISO 22000', date(2026, 10, 21), (9, 0), 240, calidad, [produccion, almacen, gerente],
         'Planta Lima', 'Revisión de los puntos críticos de control, los certificados de calidad y los registros de temperatura.'),
        ('Reunión de cierre contable de octubre', date(2026, 11, 3), (14, 0), 60, contador, [gerente, compras],
         'Oficina de contabilidad', 'Conciliación bancaria, facturas por cobrar vencidas y pagos a proveedores.'),
        ('Revisión trimestral de la cadena de frío', date(2026, 11, 12), (11, 0), 90, almacen, [calidad, produccion],
         'Cámaras de Lima y Arequipa', 'Incidentes de temperatura del trimestre, mantenimiento de los compresores y rangos de control.'),
        ('Reunión con proveedores: insumos para el verano', date(2026, 9, 24), (10, 0), 120, compras, [produccion, almacen],
         'Sala de reuniones, Planta Lima', 'Plazos de entrega y precios del cacao, la leche y los envases para la campaña de verano.'),
        ('Demostración del tablero gerencial', date(2026, 11, 18), (16, 0), 45, gerente, [ventas, almacen],
         'Oficina de gerencia, Lima', 'Revisión de las tarjetas de ventas, producción, lotes por vencer, calidad, heladeros y cadena de frío.'),
        ('Entrega del informe de calidad de octubre', date(2026, 11, 6), (9, 30), 45, calidad, [produccion, gerente],
         'Planta Lima', 'Lotes inspeccionados, aprobados y rechazados, con las acciones correctivas.'),
    ]
    for nombre, dia, hora, minutos, organizador, asistentes, lugar, descripcion in sueltas:
        crear_evento(env, nombre, dia, hora, minutos, organizador,
                     [a if a._name == 'res.partner' else a.partner_id for a in asistentes], lugar, descripcion)
        n += 1
    # Visitas y llamadas ligadas a las oportunidades (de la etapa «Propuesta» en adelante hubo una visita)
    leads = env['crm.lead'].with_context(active_test=False).search([('partner_id', '!=', False), ('type', '=', 'opportunity')], order='create_date, id')
    for lead in leads:
        datos = {**OPORTUNIDADES, **OPORTUNIDADES_NUEVAS}.get(lead.name)
        if not datos or not any(e == 'propuesta' for e, _ in datos['etapas']):
            continue
        dia_visita = next(f for e, f in datos['etapas'] if e == 'propuesta')
        while dia_visita.weekday() == 6:
            dia_visita -= timedelta(days=1)
        vendedor_lead = lead.user_id
        crear_evento(env, f'Visita comercial: {lead.partner_id.name.split(" (")[0]}', dia_visita, (rng.randint(9, 15), rng.choice([0, 30])),
                     60, vendedor_lead, [lead.partner_id], lead.partner_id.street or False,
                     'Presentación de la propuesta, muestras y condiciones de pago.', lead=lead)
        n += 1
    # Reuniones de los próximos días (para que la agenda no termine el 22/11): no se crean; todo queda dentro del periodo
    eventos = env['calendar.event'].search([])
    # Los eventos que se crearon hoy quedan fechados en su día (creación y avisos)
    env.cr.execute("UPDATE calendar_event SET create_date = start - interval '5 days', write_date = start - interval '5 days' WHERE create_date > %s", (lima(HOY, 0),))
    env.invalidate_all()
    print(f'  Calendario: {n} reuniones en la agenda ({len(eventos)} en total).')


# --- Fechas fuera de la ventana -----------------------------------------------------------------------------

def fin_de_la_ventana():
    """Primer instante después del 22/11 en hora de Lima (UTC)."""
    return lima(FIN + timedelta(days=1), 0)


def fechar_asientos_de_mano_de_obra(env):
    """Asientos «WH/MO/… - Labour» (diario de valoración): llevan el día de su orden de fabricación.

    Camino estándar: borrador → fecha → publicar. El número se limpia para que Odoo asigne el del mes que
    corresponde (STJ/2026/08/…); un asiento ya publicado no admite otra fecha con el número del mes anterior."""
    Asiento = env['account.move']
    asientos = Asiento.search([('ref', 'like', '% - Labour'), ('date', '>=', FIN + timedelta(days=1)),
                               ('state', '=', 'posted')])
    por_orden = {o.name: o for o in env['mrp.production'].search([('name', 'in', [a.ref.split(' - ')[0] for a in asientos])])}
    pendientes = sorted(((por_orden[a.ref.split(' - ')[0]].date_start.date(), a.id) for a in asientos
                         if a.ref.split(' - ')[0] in por_orden))
    for dia, asiento_id in pendientes:
        asiento = Asiento.browse(asiento_id)
        mid = ultimo_mensaje(env)
        asiento.button_draft()
        asiento.write({'name': '/', 'date': dia})
        asiento.action_post()
        fechar_mensajes(env, 'account.move', asiento.id, mid, lima(dia, 19))
    return len(pendientes)


def fechar_cierres_de_yape(env):
    """Asientos «Combine Yape POS payments…»: llevan el día en que se cerró su sesión de caja.

    Están conciliados con los pagos del PdV; pasarlos a borrador deshace esa conciliación, así que se corrige la
    fecha directamente (asiento, apuntes, pagos y conciliaciones parciales), como hace ``cargar_transacciones.py``."""
    cr = env.cr
    env.flush_all()
    cr.execute("""
        UPDATE account_move m SET date = (s.stop_at - interval '5 hours')::date
          FROM pos_session s
         WHERE m.ref LIKE 'Combine Yape POS payments from %%' AND s.stop_at IS NOT NULL
           AND s.name = substring(m.ref FROM 'Combine Yape POS payments from (.*)$') AND m.date > %(fin)s
     RETURNING m.id""", {'fin': FIN})
    ids = [fila[0] for fila in cr.fetchall()]
    if ids:
        cr.execute("UPDATE account_move_line l SET date = m.date FROM account_move m WHERE m.id = l.move_id AND m.id = ANY(%s) AND l.date <> m.date", (ids,))
        cr.execute("UPDATE account_payment p SET date = m.date FROM account_move m WHERE m.id = p.move_id AND m.id = ANY(%s) AND p.date <> m.date", (ids,))
        cr.execute("""UPDATE account_partial_reconcile r SET max_date = GREATEST(d.date, c.date)
                        FROM account_move_line d, account_move_line c
                       WHERE d.id = r.debit_move_id AND c.id = r.credit_move_id AND r.max_date > %s
                         AND (d.move_id = ANY(%s) OR c.move_id = ANY(%s))""", (FIN, ids, ids))
    env.invalidate_all()
    return len(ids)


def fechar_albaranes_del_pdv(env):
    """Los albaranes del PdV se crearon el 25/11 y su fecha prevista quedó ahí: se iguala a la de entrega."""
    env.flush_all()
    env.cr.execute("""UPDATE stock_picking SET scheduled_date = date_done
                       WHERE state = 'done' AND date_done IS NOT NULL AND date_done < %(tope)s AND scheduled_date >= %(tope)s""",
                   {'tope': fin_de_la_ventana()})
    n = env.cr.rowcount
    env.invalidate_all()
    return n


def fechar_compras_del_planificador(env):
    """Solicitudes de cotización (borrador) que generó el planificador al instalar: se fechan el 22/11.

    No son un error: los mínimos y máximos de los insumos salen del consumo semanal (HU-13) y al cierre de los
    datos las existencias de insumos son cero (la recepción de cada semana cubre lo que se consume), así que el
    planificador pide hasta el máximo (cerca de 3,6 semanas de compras, unos S/ 2,4 millones; las compras
    históricas son de S/ 663 mil por semana). Mientras las solicitudes sigan en borrador cuentan como entrada
    prevista y el cron diario no las duplica. Se conservan, solo con fecha de pedido dentro de la ventana
    (la entrega prevista sigue en diciembre, como corresponde a una compra aún sin confirmar)."""
    cr = env.cr
    env.flush_all()
    tope = fin_de_la_ventana()
    pedido = lima(FIN, 12)
    cr.execute("""UPDATE purchase_order SET date_order = %(pedido)s, date_calendar_start = %(pedido)s
                   WHERE state = 'draft' AND date_order >= %(tope)s RETURNING id""", {'pedido': pedido, 'tope': tope})
    movidas = len(cr.fetchall())
    cr.execute("""UPDATE purchase_order SET create_date = %(pedido)s - interval '1 hour', write_date = %(pedido)s
                   WHERE state = 'draft' AND create_date >= %(tope)s RETURNING id""", {'pedido': pedido, 'tope': tope})
    ids = [fila[0] for fila in cr.fetchall()]
    cr.execute("""UPDATE mail_message SET date = %(pedido)s, create_date = %(pedido)s
                   WHERE model = 'purchase.order' AND res_id = ANY(%(ids)s) AND date >= %(tope)s""",
               {'pedido': pedido, 'ids': ids, 'tope': tope})
    env.invalidate_all()
    return movidas or len(ids)


def fechar_operaciones_y_cotizaciones(env):
    """Operaciones de las órdenes terminadas (la fecha de fin quedó en la planificada, hasta 2027) y vencimiento
    de los pedidos confirmados (30 días desde su fecha, no desde la corrida)."""
    cr = env.cr
    env.flush_all()
    tope = fin_de_la_ventana()
    cr.execute("""UPDATE mrp_workorder w SET date_start = t.ini, date_finished = t.fin
                    FROM (SELECT workorder_id, MIN(date_start) AS ini, MAX(date_end) AS fin
                            FROM mrp_workcenter_productivity WHERE date_end IS NOT NULL GROUP BY 1) t
                   WHERE t.workorder_id = w.id AND w.state = 'done' AND w.date_finished >= %s""", (tope,))
    operaciones = cr.rowcount
    cr.execute("""UPDATE mrp_workorder w SET date_start = p.date_start, date_finished = p.date_finished
                    FROM mrp_production p
                   WHERE p.id = w.production_id AND w.state = 'done' AND w.date_finished >= %s AND p.date_finished < %s""", (tope, tope))
    operaciones += cr.rowcount
    cr.execute("""UPDATE sale_order SET validity_date = (date_order + interval '30 days')::date
                   WHERE state = 'sale' AND validity_date >= %s AND date_order < %s""", (FIN + timedelta(days=1), tope))
    env.invalidate_all()
    return operaciones, cr.rowcount


def fechar_tickets_de_la_mesa(env):
    """Los tres tickets abiertos que trae donofrio_base se crearon al instalar (25/11): se llevan al 21 y 22/11."""
    cr = env.cr
    nuevos = (('ticket_ti_reporte', date(2026, 11, 21), 15), ('ticket_ti_clave', date(2026, 11, 22), 9),
              ('ticket_ti_boleta_pdv', date(2026, 11, 22), 10))
    movidos = 0
    for xmlid, dia, hora in nuevos:
        ticket = ref(env, xmlid)
        if ticket.create_date < fin_de_la_ventana():
            continue
        alta = lima(dia, hora)
        ticket.date_deadline = alta + timedelta(hours=HORAS_SLA[ticket.priority])
        env.flush_all()
        cr.execute("""UPDATE project_task SET create_date = %s, write_date = %s, date_assign = %s,
                          date_last_stage_update = %s WHERE id = %s""", (alta, alta, alta, alta, ticket.id))
        cr.execute("UPDATE mail_message SET date = %s, create_date = %s WHERE model = 'project.task' AND res_id = %s",
                   (alta, alta, ticket.id))
        movidos += 1
    env.invalidate_all()
    return movidos


def traducir_textos(env):
    """Pasa a español lo que Odoo creó en inglés al correr sin idioma (``odoo shell`` usa en_US).

    Las traducciones de las referencias son las estándar de Odoo 19 (point_of_sale y mrp_account, es.po): existen,
    pero solo se aplican a lo que se genera con un usuario en español; lo ya generado se corrige aquí.
    El contacto y el empleado «Administrator» se renombran en donofrio_base (compania_data.xml)."""
    env.flush_all()
    cr = env.cr
    tarea = env['project.task'].search([('name', '=', 'Welcome Administrator!')])
    tarea.write({'name': '¡Le damos la bienvenida, Administrador!'})
    diario = env['account.journal'].search([('code', '=', 'POSS'), ('name', '=', 'Point of Sale')])
    diario.write({'name': 'Punto de venta'})
    combinar = (r'Combine (.*) POS payments from (.*)$', r'Combinar pagos de \1 del PdV de \2')
    mano_de_obra = (r' - Labour$', ' - Mano de obra')
    pago_manual = (r'^Manual Payment: ', 'Pago manual: ')
    cambiados = 0
    for tabla, columna in (('account_move', 'ref'), ('account_move_line', 'name'), ('account_move_line', 'ref'),
                           ('account_payment', 'memo')):
        for patron, nuevo in (combinar, mano_de_obra, pago_manual):
            cr.execute(f"UPDATE {tabla} SET {columna} = regexp_replace({columna}, %s, %s) WHERE {columna} ~ %s",  # noqa: S608
                       (patron, nuevo, patron))
            cambiados += cr.rowcount if tabla == 'account_move' else 0
    env.invalidate_all()
    return len(tarea) + len(diario), cambiados


def ajustar_plazo_de_tickets(env):
    """Tickets abiertos de la mesa con fecha límite posterior al 22/11.

    Si ya están en análisis o más allá, se resuelven ese día (dentro de su plazo, SLA cumplido); los que siguen
    en «Nuevo» se llevan a una fecha de creación tal que su plazo venza el 22/11 (quedan con el SLA vencido)."""
    mesa = ref(env, 'proyecto_mesa_servicios')
    tope = fin_de_la_ventana()
    tickets = env['project.task'].search([('project_id', '=', mesa.id), ('date_end', '=', False),
                                          ('date_deadline', '>=', tope)], order='id')
    nuevo, resuelto = ref(env, 'etapa_ti_nuevo'), ref(env, 'etapa_ti_resuelto')
    cr = env.cr
    for indice, ticket in enumerate(tickets):
        if ticket.stage_id != nuevo:
            cierre = lima(FIN, 11 + indice)
            mid = ultimo_mensaje(env)
            ticket.write({'stage_id': resuelto.id, 'state': '1_done'})
            ticket.write({'date_end': cierre})
            ticket.message_post(body='Atendido y verificado con el usuario.',
                                message_type='comment', subtype_xmlid='mail.mt_note')
            fechar_mensajes(env, 'project.task', ticket.id, mid, cierre)
            env.flush_all()
            cr.execute("UPDATE project_task SET date_last_stage_update = %s WHERE id = %s", (cierre, ticket.id))
        else:
            limite = lima(FIN, 12 + indice)
            alta = limite - timedelta(hours=HORAS_SLA[ticket.priority])
            ticket.date_deadline = limite
            env.flush_all()
            cr.execute("""UPDATE project_task SET create_date = %s, write_date = %s, date_assign = %s,
                              date_last_stage_update = %s WHERE id = %s""", (alta, alta, alta, alta, ticket.id))
            cr.execute("UPDATE mail_message SET date = %s, create_date = %s WHERE model = 'project.task' AND res_id = %s AND date > %s",
                       (alta, alta, ticket.id, alta))
    env.invalidate_all()
    return len(tickets)


def cargar_ajustes(env):
    textos, referencias = traducir_textos(env)
    tickets = ajustar_plazo_de_tickets(env)
    print(f'  Ajustes: {textos} textos renombrados, {referencias} asientos con referencia en español y '
          f'{tickets} tickets abiertos con plazo fuera de la ventana corregidos.')


def cargar_fechas(env):
    asientos = fechar_asientos_de_mano_de_obra(env)
    yape = fechar_cierres_de_yape(env)
    albaranes = fechar_albaranes_del_pdv(env)
    compras = fechar_compras_del_planificador(env)
    operaciones, cotizaciones = fechar_operaciones_y_cotizaciones(env)
    tickets = fechar_tickets_de_la_mesa(env)
    print(f'  Fechas: {asientos} asientos de mano de obra, {yape} cierres de Yape, {albaranes} albaranes del PdV, '
          f'{compras} solicitudes de compra, {operaciones} operaciones de órdenes, {cotizaciones} cotizaciones y '
          f'{tickets} tickets llevados a la ventana.')


# --- Programa principal -------------------------------------------------------------------------------------

PROCEDIMIENTOS = {'contactos': cargar_contactos, 'crm': cargar_crm, 'calidad': cargar_calidad,
                  'heladeros': cargar_heladeros, 'frio': cargar_frio, 'mesa': cargar_mesa, 'calendario': cargar_calendario,
                  'fechas': cargar_fechas, 'ajustes': cargar_ajustes}


def fechar_rezagados(env, desde):
    """Al volcar al final, Odoo recalcula el teléfono y el correo de las oportunidades (vienen del cliente) y deja
    un aviso de seguimiento con la fecha de hoy: se fecha al cierre de la oportunidad."""
    env.flush_all()
    env.cr.execute("""UPDATE mail_message m SET date = COALESCE(l.date_closed, l.date_last_stage_update, l.create_date)
                        FROM crm_lead l WHERE m.model = 'crm.lead' AND m.res_id = l.id AND m.id > %s AND m.date > %s""",
                   (desde, lima(FIN, 23)))
    # El aviso «Oportunidad creada» de las 20 oportunidades originales quedó con la fecha de la carga inicial
    env.cr.execute("""UPDATE mail_message m SET date = l.create_date
                        FROM crm_lead l, mail_message_subtype st
                       WHERE m.model = 'crm.lead' AND m.res_id = l.id AND st.id = m.subtype_id
                         AND st.id = %s AND m.date > %s AND l.create_date < %s""",
                   (env.ref('crm.mt_lead_create').id, lima(FIN, 23), lima(FIN, 23)))
    env.invalidate_all()
    env.cr.commit()


def main(env):
    antes = conteos(env)
    mensaje_inicial = ultimo_mensaje(env)
    print(f'Demostración completa: {INICIO:%d/%m/%Y} → {FIN:%d/%m/%Y} (semilla {SEMILLA}, referencia {HOY:%d/%m/%Y})')
    for parte in PARTES:
        if parte not in PARTES_A_CARGAR:
            continue
        if marca(env, parte):
            print(f'  {parte}: ya cargada (parámetro {PARAMETRO}{parte}); no se repite.')
            continue
        PROCEDIMIENTOS[parte](env)
        marcar(env, parte)
        env.cr.commit()
    fechar_rezagados(env, mensaje_inicial)
    despues = conteos(env)
    print('Conteos por modelo (antes → después):')
    for modelo, n in antes.items():
        print(f'  {modelo:<32} {n:>7} → {despues[modelo]:>7}')


# `env` existe cuando el archivo se ejecuta con `odoo shell`; al importarlo (pruebas) no se ejecuta nada
if 'env' in globals():
    main(env)  # noqa: F821
