# -*- coding: utf-8 -*-
{
    'name': 'Daftar Jurnal Ilmiah',
    'version': '1.0.0',
    'summary': 'Daftar jurnal ilmiah nasional & internasional',
    'description': """
Daftar Jurnal Ilmiah (Nasional & Internasional)
===============================================

Modul untuk mengelola dan menampilkan daftar jurnal ilmiah nasional dan internasional dengan fitur:

* Manajemen jurnal dengan impact factor
* Indexing (Scopus, Web of Science, SINTA)
* Publikasi website dengan halaman khusus (/jurnal)
* Kategorisasi dan tagging
* SEO optimization
* Responsive design
    """,
    'category': 'Website/Website',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'website', 'website_blog', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/jurnal_data.xml',
        'views/jurnal_views.xml',
        'templates/jurnal_templates.xml',
        'views/jurnal_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}