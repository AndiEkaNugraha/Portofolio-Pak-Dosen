# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Daftar HKI & Paten',
    'version': '1.0.0',
    'summary': 'Daftar Hak Kekayaan Intelektual & Paten',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/hki_data.xml',
        'views/hki_views.xml',
        'templates/hki_templates.xml',
        'views/hki_menus.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}