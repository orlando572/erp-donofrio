def post_init_hook(env):
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
