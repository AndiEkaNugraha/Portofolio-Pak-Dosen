# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Daftar Mata Kuliah',
    'version': '1.0.0',
    'summary': 'Daftar mata kuliah yang diampu dengan penjelasan, silabus, dan informasi lainnya',
    'description': """
        Modul untuk mengelola daftar mata kuliah (courses) yang diampu oleh dosen dengan fitur:
        - Informasi lengkap mata kuliah (kode, nama, SKS, semester)
        - Deskripsi dan silabus mata kuliah
        - Tujuan pembelajaran (learning outcomes)
        - Metode pembelajaran dan penilaian
        - Referensi dan materi pembelajaran
        - Jadwal kelas
        - Publikasi di halaman website /mata-kuliah
        - SEO optimization untuk setiap mata kuliah

        Required:
        - Website Blog module must be installed first
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail', 'website_blog'],
    'data': [
        'security/ir.model.access.csv',
        'data/matakuliah_data.xml',
        # 'data/website_data.xml',  # Disabled - has validation issues
        'views/matakuliah_views_clean.xml',
        'views/matakuliah_menus.xml',
        'templates/matakuliah_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'matakuliah/static/src/css/style.css',
        ],
    },
    'installable': False,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
