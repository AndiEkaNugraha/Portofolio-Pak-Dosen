# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Hibah & Pendanaan',
    'version': '1.0.0',
    'summary': 'Dokumentasi Hibah dan Pendanaan Penelitian untuk Portfolio Dosen',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/hibah_pendanaan_data.xml',
        'views/hibah_pendanaan_views.xml',
        'views/hibah_pendanaan_menus.xml',
        'templates/hibah_pendanaan_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # Add CSS/JS assets if needed
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}