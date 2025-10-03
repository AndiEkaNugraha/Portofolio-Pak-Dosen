# -*- coding: utf-8 -*-
{
    'name': 'Daftar HKI & Paten',
    'version': '1.0.0',
    'summary': 'Daftar Hak Kekayaan Intelektual & Paten',
    'description': """
Daftar HKI & Paten (Hak Kekayaan Intelektual & Paten)
=====================================================

Modul untuk mengelola dan menampilkan daftar HKI & Paten dengan fitur:

* Manajemen HKI dengan detail lengkap (Hak Cipta, Paten, Merek, Desain Industri)
* Kategorisasi berdasar jenis dan bidang keilmuan
* Publikasi website dengan halaman khusus (/hki)
* Informasi status dan registrasi
* SEO optimization
* Responsive design
* Filter berdasar tahun, kategori, status, dan jenis HKI
    """,
    'category': 'Website/Website',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/hki_data.xml',
        'views/hki_views.xml',
        'templates/hki_templates.xml',
        'views/hki_menus.xml',
    ],
    'demo': [
        # 'demo/hki_demo_simple.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}