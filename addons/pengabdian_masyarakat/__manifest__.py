# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Daftar Kegiatan Pengabdian',
    'version': '1.0.0',
    'summary': 'Daftar Kegiatan Pengabdian Masyarakat',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'website_blog', 'mail', 'hibah_pendanaan'],
    'data': [
        'security/ir.model.access.csv',
        'data/pengabdian_data.xml',
        'views/pengabdian_views.xml',
        'templates/pengabdian_templates.xml',
        'views/pengabdian_menus.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}