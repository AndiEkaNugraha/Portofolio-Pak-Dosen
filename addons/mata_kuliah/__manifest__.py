# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Mata Kuliah',
    'version': '1.0.0',
    'summary': 'Daftar mata kuliah yang pernah dihandle dosen',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/academic_year_data.xml',
        'data/mata_kuliah_data.xml',
        'views/academic_year_views.xml',
        'views/mata_kuliah_views.xml',
        'templates/mata_kuliah_templates.xml',
        'views/mata_kuliah_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}