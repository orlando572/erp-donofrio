{
    'name': "D'Onofrio Calidad",
    'summary': "Inspecciones de calidad por puntos de control, ligadas a la orden de producción y al lote (M1)",
    'description': """
Módulo propio de la Fase 2 (M1). La Calidad estándar de Odoo es Enterprise, así que este módulo
crea los puntos de control, las inspecciones con sus mediciones y el bloqueo del despacho de un lote rechazado.
Todos los datos son ficticios.
""",
    'author': "Evelyn y Orlando (UTP Arequipa)",
    'website': 'https://github.com/orlando572/erp-donofrio',
    'category': 'Manufacturing',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['donofrio_base', 'mrp', 'stock', 'product_expiry'],
    'data': [
        'security/donofrio_calidad_security.xml',
        'security/ir.model.access.csv',
        'data/calidad_data.xml',
        'views/calidad_views.xml',
        'report/calidad_report.xml',
    ],
    'installable': True,
    'application': True,
}
