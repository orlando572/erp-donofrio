{
    'name': "D'Onofrio Heladeros",
    'summary': "Liquidación diaria del heladero concesionario: despachado, devuelto, merma, vendido, importe y comisión (M2)",
    'description': """
Módulo propio de la Fase 2 (M2). El heladero compra a precio de heladero y liquida cada día.
Al confirmar la liquidación crea y confirma el pedido de venta de lo vendido.
Todos los datos son ficticios.
""",
    'author': "Evelyn y Orlando (UTP Arequipa)",
    'website': 'https://github.com/orlando572/erp-donofrio',
    'category': 'Sales',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['donofrio_base', 'sale_management', 'stock'],
    'data': [
        'security/donofrio_heladeros_security.xml',
        'security/ir.model.access.csv',
        'data/heladeros_data.xml',
        'views/liquidacion_views.xml',
    ],
    'installable': True,
    'application': True,
}
