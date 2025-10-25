# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Daftar Jurnal Ilmiah',
    'version': '1.0.0',
    'summary': 'Daftar jurnal ilmiah nasional & internasional',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/jurnal_data.xml',
        'views/jurnal_views.xml',
        'templates/jurnal_templates.xml',
        'views/jurnal_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}