# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name' : 'Multi Branch',
    'version' : '1.0',
    'author':'Craftsync Technologies',
    'category': 'Manufacturing',
    'maintainer': 'Craftsync Technologies',
   
    'summary': """Manage Multiple Branches, Operating units""",

    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'depends' : ['hr','account','stock','mrp','sale','purchase','web','project'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/branch.xml',
        'views/warehouse.xml',
        'views/product.xml',
        'views/mrp.xml',
        'views/purchase.xml',
        'views/user.xml',
        'views/employee.xml',
        'views/partner.xml',
        'views/res_config_settings_views.xml',
        'views/invoice.xml',
        'views/picking.xml',
        'views/project.xml',
        'views/sale.xml',

    ],
    'qweb': ['static/xml/*.xml'],    

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'price': 39.99,
    'currency': 'USD',

}
