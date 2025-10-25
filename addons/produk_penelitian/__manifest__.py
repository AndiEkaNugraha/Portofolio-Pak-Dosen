# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Prototipe & Produk Penelitian',
    'version': '1.0.0',
    'summary': 'Daftar Prototipe dan Produk Hasil Penelitian',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/produk_data.xml',
        'views/produk_views.xml',
        'templates/produk_templates.xml',
        'views/produk_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}