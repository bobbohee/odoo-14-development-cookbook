# -*- coding: utf-8 -*-
{
    'name': "My Library",
    'summary': """Manage books easily""",
    'author': "bobbohee",
    'category': 'Library',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_book_menus.xml',
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
