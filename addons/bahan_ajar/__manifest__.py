# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - E-Learning & Bahan Ajar',
    'version': '1.0.0',
    'summary': 'Manajemen materi pembelajaran digital, termasuk PDF, video, dan sumber daya online',
    'description': """
        Modul untuk mengelola bahan ajar dan materi pembelajaran (e-learning) dengan fitur:
        - Upload dan manajemen file PDF (modul, handout, slide)
        - Embed video pembelajaran (YouTube, Vimeo, dll)
        - Link ke sumber belajar online (website, LMS, dll)
        - Pengelompokan materi per mata kuliah dan topik
        - Deskripsi dan metadata materi pembelajaran
        - Tracking download dan statistik penggunaan
        - SEO optimization untuk setiap materi
        - Tampilan responsif di website

        Required:
        - Website Blog module must be installed first
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail', 'website_blog'],
    'data': [
        'security/ir.model.access.csv',
        'data/blog_data.xml',
        'views/bahan_ajar_views.xml',
        'views/bahan_ajar_menus.xml',
        'views/blog_templates.xml',
        'templates/bahan_ajar_templates.xml',
        'data/website_data.xml',],
    'demo': [
        'data/bahan_ajar_demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bahan_ajar/static/src/css/style.css',
        ],
    },
    'installable': False,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}