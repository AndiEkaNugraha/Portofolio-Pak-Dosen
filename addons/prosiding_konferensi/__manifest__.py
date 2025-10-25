# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Daftar Prosiding Konferensi',
    'version': '1.0.0',
    'summary': 'Daftar prosiding konferensi nasional & internasional',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/prosiding_data.xml',
        'views/prosiding_views.xml',
        'templates/prosiding_templates.xml',
        'views/prosiding_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}