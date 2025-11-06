# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Informasi Bimbingan Mahasiswa',
    'version': '1.0.0',
    'summary': 'Manajemen informasi bimbingan dan pembimbing akademik mahasiswa',
    'description': """
        Modul untuk mengelola informasi bimbingan mahasiswa dengan fitur:
        - Daftar mahasiswa yang dibimbing
        - Tracking status bimbingan
        - Tema/topik bimbingan
        - Jadwal bimbingan
        - Output/hasil bimbingan
        - Statistik bimbingan
        - Tampilan responsif di website
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/bimbingan_data.xml',
        'views/bimbingan_views.xml',
        'views/bimbingan_menus.xml',
        'templates/bimbingan_templates.xml',
    ],
    'demo': [
        'data/bimbingan_demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bimbingan_mahasiswa/static/src/css/style.css',
        ],
    },
    'installable': False,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
