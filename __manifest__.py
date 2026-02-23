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
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    # Por qué: ceralfa_studio_migration debe cargar primero para limpiar
    #          vistas heredadas rotas (ocapi_bindings) antes de validar las nuestras.
    'depends': ['base', 'account', 'sale', 'ceralfa_studio_migration'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # Odoo 19: account.tax_groups_totals eliminado, revisar templates
        # 'views/grupos_impuestos.xml',
        'views/account_move_view.xml',
        # Odoo 19: verificar si account.document_tax_totals y l10n_ar.report_invoice_document siguen existiendo
        # 'views/templates_factura_usd.xml',
        # 'views/templates_sale_usd.xml',
        'views/views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

