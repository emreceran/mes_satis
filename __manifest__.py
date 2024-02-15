# -*- coding: utf-8 -*-
{
    'name': "mes_satis_v1",

    'summary': """
        Her ürüne bir adam saat değeri eklenir ve sale order satırlarında ve teklif
         toplamında gösterilerek satış teklifcisine ne kadar adam saat değeri harcanacağı
          bilgisi verilir. Ayrıca satış siparişinde maliyetlere yüzde olarak indirim imkanı sağlanır
        """,

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
    'depends': ['base',
                'sale_management',
                'sale_margin',
                'account',
                'hr_expense',
                'stock',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/product_form_view.xml',
        'views/order_line_disc.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
