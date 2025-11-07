# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Aktivitas Reviewer',
    'version': '1.0.0',
    'summary': 'Daftar Aktivitas Review Dosen',
    'description': """
        Modul untuk mengelola aktivitas review dosen meliputi:
        - Review Jurnal Ilmiah
        - Review Buku dan Naskah
        - Review Penelitian
        - Review Proposal
        - Review Artikel Konferensi
        - Review Tugas Akhir/Disertasi
        - Dan jenis review lainnya
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/reviewer_data.xml',
        'views/reviewer_views.xml',
        'templates/reviewer_templates.xml',
        'views/reviewer_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
