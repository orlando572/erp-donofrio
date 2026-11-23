{
    'name': "D'Onofrio Base",
    'summary': "Configuración y datos maestros de D'Onofrio (helados y confitería)",
    'description': """
Módulo base del ERP académico de D'Onofrio sobre Odoo 19 Community.
Carga por código la configuración y los datos maestros de cada área.
Todos los datos (RUC, clientes, empleados, precios) son ficticios.
""",
    'author': "Evelyn y Orlando (UTP Arequipa)",
    'website': 'https://github.com/orlando572/erp-donofrio',
    'category': 'Customizations',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'l10n_pe', 'stock', 'sale', 'purchase', 'mrp', 'point_of_sale'],
    'data': [
        'data/compania_data.xml',
        'data/almacenes_data.xml',
        'security/donofrio_security.xml',
        'data/usuarios_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
