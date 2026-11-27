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
    'depends': ['base', 'l10n_pe', 'stock', 'sale', 'purchase', 'purchase_stock', 'mrp', 'point_of_sale', 'product_expiry',
                'crm', 'hr', 'hr_org_chart', 'project',
                'spreadsheet_dashboard_sale', 'spreadsheet_dashboard_stock_account', 'spreadsheet_dashboard_account',
                # HU-27: 2FA, política de contraseñas y auditoría de cambios (OCA, fijado en el Dockerfile)
                'auth_totp_mail', 'auth_password_policy', 'auditlog'],
    'data': [
        'data/compania_data.xml',
        'data/almacenes_data.xml',
        'security/donofrio_security.xml',
        'security/ir.model.access.csv',
        'data/usuarios_data.xml',
        'data/productos_data.xml',
        'data/crm_data.xml',
        'data/precios_data.xml',
        'data/produccion_data.xml',
        'data/reabastecimiento_data.xml',
        'data/clientes_data.xml',
        'data/rrhh_data.xml',
        'data/vistas_gerencia_data.xml',
        'data/mesa_servicios_data.xml',
        'data/seguridad_data.xml',
        'data/idioma_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
