# -*- coding: utf-8 -*-
{
    'name': 'Daftar Prosiding Konferensi',
    'version': '1.0.0',
    'summary': 'Daftar prosiding konferensi nasional & internasional',
    'description': """
Daftar Prosiding Konferensi (Nasional & Internasional)
======================================================

Modul untuk mengelola dan menampilkan daftar prosiding konferensi nasional dan internasional dengan fitur:

* Manajemen konferensi dengan detail lengkap
* Kategorisasi berdasar bidang keilmuan
* Publikasi website dengan halaman khusus (/prosiding)
* Informasi akreditasi dan indexing
* SEO optimization
* Responsive design
* Filter berdasar tahun, kategori, dan akreditasi
    """,
    'category': 'Website/Website',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/prosiding_data.xml',
        'views/prosiding_views.xml',
        'templates/prosiding_templates.xml',
        'views/prosiding_menus.xml',
    ],
    'demo': [
        'demo/prosiding_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}