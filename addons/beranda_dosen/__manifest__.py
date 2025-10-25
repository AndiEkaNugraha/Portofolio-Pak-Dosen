# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Beranda Dosen - Profile & Portfolio Homepage',
    'version': '1.0.3',
    'summary': 'Homepage Beranda dengan Profil Dosen dan Portfolio',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/beranda_data.xml',
        'views/beranda_views.xml',
        'templates/beranda_templates.xml',
        'views/beranda_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}