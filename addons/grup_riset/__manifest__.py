# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Grup Riset & Laboratorium',
    'version': '1.0.0',
    'summary': 'Manajemen Grup Riset dan Laboratorium untuk Portfolio Dosen',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/grup_riset_data.xml',
        'views/grup_riset_views.xml',
        'templates/grup_riset_templates.xml',
        'views/grup_riset_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}