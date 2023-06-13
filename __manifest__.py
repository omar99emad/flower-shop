# -*- coding: utf-8 -*-
{
    'name': "flower_shop",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','product','stock','web','website_sale','base_geolocalize',],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/flower_flower_views.xml',
        'views/product_product_views.xml',
        'views/template_product_inhert.xml',
        'views/flower_water_views.xml',
        'views/stock_production_lot_inhert.xml',
        'views/warehouse_weather_views.xml',
        'views/stock_warehouse_views.xml',
        'reports/flower_sale_order_views.xml',
        'data/ir_cron.xml',
        'data/ir_actions_server.xml',
        'data/ir_config_parameter_data.xml'
    
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
