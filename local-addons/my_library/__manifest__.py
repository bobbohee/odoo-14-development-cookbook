# -*- coding: utf-8 -*-
{
    'name': "My Library",
    'summary': """Manage books easily""",
    'author': "bobbohee",
    'category': 'Library',
    'version': '13.0.1.0.1',
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_book_rent_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/library_book_rent_wizard.xml',
        'views/library_book_menus.xml',
        'data/data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    # 'auto_install': True
    # 'installable': True,
    # 'external_dependencies': {
    #     'python': [],
    # },
    # 'pre_init_hook': '함수',
    # 'post_init_hook': '함수',
    # 'uninstall_hook': '함수',
}
