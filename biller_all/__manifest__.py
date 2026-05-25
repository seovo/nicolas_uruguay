# -*- coding: utf-8 -*-
{

    'name': 'Biller all',

    'version': '1.2.2',

    'category': '',

    'summary': 'Modulo para instalar todos los modulos destinados a la integracion con Biller v2',

    'author': 'Jon Horton',

    'website': '',

    'depends': [
        'account',
    ],

    'data': [

        'security/ir.model.access.csv',
        'wizard/get_documents_wizard_views.xml',
        'views/biller_record_views.xml',
        'views/account_move_view.xml',
        'views/product_template_views.xml',
        'views/res_company_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'data/received_docs_cron.xml',
    ],

    'installable': True,

    'auto_install': False,

    'application': True,

    'description': """
Biller all
===========================
Modulo que integra Odoo con los servicios provistos por biller.uy. Al agregarle en los atributos de la compañia, 
la sucursal y token provistos por Biller, todas las facturas publicadas en Odoo pasaran a ser tambien publicadas en Biller.
Asi mismo, las facturas emitidas por Biller hacia uno, seran diariamente creadas en Odoo automaticamente.   
""",

}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
