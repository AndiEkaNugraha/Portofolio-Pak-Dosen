# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Proyek Penelitian',
    'version': '1.0.0',
    'summary': 'Manajemen Proyek Penelitian Aktif & Terdahulu untuk Portfolio Dosen',
    'description': """""",
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'buku_karya', 'jurnal_ilmiah', 'produk_penelitian', 'hki_paten', 'prosiding_konferensi'],
    'data': [
        'security/ir.model.access.csv',
        'data/proyek_penelitian_data.xml',
        'views/proyek_penelitian_views.xml',
        'views/proyek_penelitian_menus.xml',
        'templates/proyek_penelitian_templates.xml',
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