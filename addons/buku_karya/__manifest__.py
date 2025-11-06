# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Daftar Buku',
    'version': '1.0.0',
    'summary': 'Daftar Buku Publikasi',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/buku_data.xml',
        'views/buku_views.xml',
        'templates/buku_templates.xml',
        'views/buku_menus.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}