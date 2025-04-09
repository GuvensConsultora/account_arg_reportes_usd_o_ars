# -*- coding: utf-8 -*-
{
    'name': "factura_en_usd",

    'summary': "Generar reporte en dolares sin afectar factura en pesos",

    'description': """
Generación de un reporte pdf teniendo en cuanto dos campos agregados tc y fact en usd 
    """,

    'author': "Güvens Consultora",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/grupos_impuestos.xml',
        'views/account_move_view.xml',
        'views/templates_factura_usd.xml', 
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

