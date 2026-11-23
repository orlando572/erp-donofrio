import logging
import os

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Pasos que no se pueden expresar como datos XML y corren al instalar el módulo."""
    _asignar_clave_a_usuarios(env)
    _asignar_responsable_de_inventario(env)
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

    env.registry._auto_install_template = cargar_plan_contable
