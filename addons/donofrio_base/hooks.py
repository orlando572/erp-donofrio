import logging
import os

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Pasos que no se pueden expresar como datos XML y corren al instalar el módulo."""
    _asignar_clave_a_usuarios(env)
    _asignar_responsable_de_inventario(env)
    _configurar_valoracion(env)
    _programar_plan_contable(env)


def _asignar_clave_a_usuarios(env):
    """Pone la contraseña de prueba (variable DONOFRIO_USER_PASSWORD de .env) a los usuarios del módulo.

    La contraseña nunca va en el código ni en los datos. Si la variable no existe, los usuarios
    quedan sin contraseña (no pueden iniciar sesión) y se avisa en el registro.
    """
    ids = env['ir.model.data'].search([
        ('module', '=', 'donofrio_base'),
        ('model', '=', 'res.users'),
    ]).mapped('res_id')
    usuarios = env['res.users'].browse(ids)
    clave = os.environ.get('DONOFRIO_USER_PASSWORD')
    if not clave:
        _logger.warning(
            'DONOFRIO_USER_PASSWORD no está definida: los %s usuarios de donofrio_base quedan sin contraseña.',
            len(usuarios),
        )
        return
    usuarios.write({'password': clave})


def _asignar_responsable_de_inventario(env):
    """HU-11: el jefe de almacén es el responsable de todos los terminados e insumos.

    Odoo crea la actividad «Alerta de vencimiento» (30 días antes en los terminados) a nombre del
    responsable del producto; sin él, la actividad iría al superusuario y nadie la vería.
    """
    jefe = env.ref('donofrio_base.user_jefe_almacen')
    categorias = env.ref('donofrio_base.cat_terminados') | env.ref('donofrio_base.cat_insumos')
    productos = env['product.template'].search([('categ_id', 'child_of', categorias.ids)])
    productos.write({'responsible_id': jefe.id})


def _configurar_valoracion(env):
    """HU-14: valoración FIFO en terminados e insumos (03 §3.3 b).

    Con FIFO, al terminar una OP el costo unitario del lote producido sale de lo que costaron los
    insumos consumidos más el costo por hora de los centros de trabajo (``mrp_account``).
    """
    categorias = env['product.category'].search([
        ('id', 'child_of', (env.ref('donofrio_base.cat_terminados') | env.ref('donofrio_base.cat_insumos')).ids),
    ])
    categorias.write({'property_cost_method': 'fifo', 'property_valuation': 'real_time'})


# Cuenta de contrapartida de cada ubicación virtual (plan contable PE). En Odoo 19 la valoración solo genera
# asientos si la ubicación de origen o destino tiene cuenta; ``l10n_pe`` no las trae. Simplificación del
# proyecto: una sola cuenta por ubicación virtual (la variación de existencias 7111 sirve a producción y ajustes).
CUENTAS_DE_UBICACIONES = {
    'supplier': '6020000',    # compras de materias primas
    'production': '7111000',  # variación de productos terminados
    'inventory': '7111000',   # ajustes de inventario
    'customer': '6922100',    # costo de ventas de productos terminados (venta local)
}
CUENTAS_DE_CATEGORIAS = {
    'donofrio_base.cat_terminados': '2111100',     # productos terminados
    'donofrio_base.cat_insumos': '2411100',        # materias primas
}


def _cuenta(env, codigo):
    cuenta = env['account.account'].search([('code', '=', codigo)], limit=1)
    if not cuenta:
        _logger.warning('No existe la cuenta %s en el plan contable: se omite.', codigo)
    return cuenta


def _configurar_cuentas_de_valoracion(env):
    """HU-14: cuentas de valoración por categoría y de contrapartida por ubicación virtual (asientos de stock)."""
    compania = env.ref('base.main_company')
    for uso, codigo in CUENTAS_DE_UBICACIONES.items():
        cuenta = _cuenta(env, codigo)
        if cuenta:
            env['stock.location'].search([
                ('usage', '=', uso), ('company_id', 'in', (False, compania.id)),
            ]).valuation_account_id = cuenta
    for xmlid, codigo in CUENTAS_DE_CATEGORIAS.items():
        cuenta = _cuenta(env, codigo)
        if cuenta:
            raiz = env.ref(xmlid)
            env['product.category'].search([('id', 'child_of', raiz.id)]).property_stock_valuation_account_id = cuenta


def _programar_plan_contable(env):
    """Carga el plan contable peruano (plantilla ``pe`` de ``l10n_pe``) en la compañía principal.

    Se hace aquí y no en un XML porque, al instalar ``l10n_pe`` con la compañía aún sin país,
    Odoo no elige ninguna plantilla. Ahora que ``compania_data.xml`` ya puso el país (PE),
    se usa el mismo mecanismo con el que ``account`` carga la plantilla al instalar un módulo
    de localización: se ejecuta al terminar de cargar el registro (``_register_hook``).
    Solo corre al instalar el módulo, no en las actualizaciones (``-u``).
    """

    def cargar_plan_contable(env):
        compania = env.ref('base.main_company')
        if compania.chart_template != 'pe':
            env['account.chart.template'].try_loading('pe', compania)
        _configurar_cuentas_de_valoracion(env)
        crear_punto_de_venta(env)

    env.registry._auto_install_template = cargar_plan_contable


def crear_punto_de_venta(env):
    """HU-10: crea el PdV «Heladería Av. Venezuela» con pago en efectivo y Yape (03 §3.3 a).

    Va en el hook y no en un XML porque necesita los diarios y cuentas del plan contable, que se
    cargan al terminar de instalar el módulo (ver ``_programar_plan_contable``). Es idempotente.
    """
    _habilitar_productos_en_pdv(env)
    if env.ref('donofrio_base.pos_config_venezuela', raise_if_not_found=False):
        return
    compania = env.ref('base.main_company')
    Diario = env['account.journal']
    efectivo = Diario.create({'name': 'Efectivo PdV', 'type': 'cash', 'code': 'EFEPV', 'company_id': compania.id})
    yape = Diario.create({'name': 'Yape', 'type': 'bank', 'code': 'YAPE', 'company_id': compania.id})
    Metodo = env['pos.payment.method']
    metodo_efectivo = Metodo.create({'name': 'Efectivo', 'journal_id': efectivo.id, 'company_id': compania.id})
    metodo_yape = Metodo.create({'name': 'Yape', 'journal_id': yape.id, 'company_id': compania.id})
    config = env['pos.config'].create({
        'name': 'Heladería Av. Venezuela',
        'company_id': compania.id,
        'picking_type_id': env.ref('stock.warehouse0').pos_type_id.id,
        'payment_method_ids': [(6, 0, (metodo_efectivo | metodo_yape).ids)],
    })
    env['ir.model.data']._update_xmlids([
        {'xml_id': f'donofrio_base.{nombre}', 'record': registro, 'noupdate': True}
        for nombre, registro in (
            ('diario_efectivo_pdv', efectivo), ('diario_yape', yape),
            ('pdv_metodo_efectivo', metodo_efectivo), ('pdv_metodo_yape', metodo_yape),
            ('pos_config_venezuela', config),
        )
    ])


def _habilitar_productos_en_pdv(env):
    """Marca los productos terminados como disponibles en el PdV; sin esto el catálogo del cajero sale vacío.

    Los insumos no se venden en mostrador. Se hace aquí y no en ``productos_data.xml`` porque esos
    registros son ``noupdate`` y un XML no los cambiaría en una base que ya existe.
    """
    terminados = env['product.template'].search([
        ('categ_id', 'child_of', env.ref('donofrio_base.cat_terminados').id),
        ('available_in_pos', '=', False),
    ])
    terminados.write({'available_in_pos': True})
