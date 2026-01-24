# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Bimbingan Mahasiswa',
    'version': '1.0.3',
    'summary': 'Pengajuan Bimbingan Mahasiswa',
    'description': """
        Modul untuk mengelola pengajuan bimbingan mahasiswa oleh dosen meliputi:
        - Bimbingan Akademik
        - Bimbingan Skripsi
        - Bimbingan Tesis
        - Bimbingan Disertasi
        - Dan jenis bimbingan lainnya
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'portal', 'mail'],
    'data': [
        'security/guidance_security.xml',
        'security/ir.model.access.csv',
        'data/bimbingan_data.xml',
        'views/bimbingan_views.xml',
        'templates/bimbingan_templates.xml',
        'views/bimbingan_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}