import logging
import os

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Pasos que no se pueden expresar como datos XML y corren al instalar el módulo."""
    _asignar_clave_a_usuarios(env)
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
        crear_punto_de_venta(env)

    env.registry._auto_install_template = cargar_plan_contable


def crear_punto_de_venta(env):
    """HU-10: crea el PdV «Heladería Av. Venezuela» con pago en efectivo y Yape (03 §3.3 a).

    Va en el hook y no en un XML porque necesita los diarios y cuentas del plan contable, que se
    cargan al terminar de instalar el módulo (ver ``_programar_plan_contable``). Es idempotente.
    """
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
