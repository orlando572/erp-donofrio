{
    'name': "D'Onofrio Tablero",
    'summary': "Tablero gerencial de KPIs (acción OWL) y marca visual del backend (M4)",
    'description': """
Módulo propio de la Fase 2 (M4). Un tablero de solo lectura con tarjetas de KPI y un gráfico mensual de ventas,
con filtro por almacén. Las tarjetas de calidad, heladeros y cadena de frío salen solo si su módulo está instalado.
Incluye el color de marca y el favicon del backend. Todos los datos son ficticios.
""",
    'author': "Evelyn y Orlando (UTP Arequipa)",
    'website': 'https://github.com/orlando572/erp-donofrio',
    'category': 'Productivity',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['donofrio_base', 'web', 'sale', 'stock', 'mrp', 'product_expiry'],
    'data': [
        'views/tablero_views.xml',
        'views/layout_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('prepend', 'donofrio_tablero/static/src/scss/primary_variables.scss'),
        ],
        'web.assets_backend': [
            'donofrio_tablero/static/src/tablero/*',
        ],
    },
    'installable': True,
    'application': True,
}
