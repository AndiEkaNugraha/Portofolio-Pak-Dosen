# -*- coding: utf-8 -*-
{
    'name': 'Profil Dosen',
    'version': '1.0.0',
    'summary': 'Profil Lengkap Dosen dengan Biografi, Pendidikan, Keahlian, Pengalaman, Penghargaan, dan CV Download',
    'description': """
        Modul untuk mengelola profil dosen dengan fitur:
        - Biografi lengkap dengan foto
        - Riwayat pendidikan (S1, S2, S3)
        - Bidang keahlian & minat riset
        - Riwayat pekerjaan/pengalaman
        - Daftar penghargaan & pengakuan
        - Upload dan download file CV
        - Media sosial & kontak online
        - SEO optimization untuk website
        - Publikasi profil di halaman website /profil-dosen
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/profil_data.xml',
        'views/profil_views.xml',
        'templates/profil_templates.xml',
        'views/profil_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'profil_dosen/static/src/css/profil_style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
