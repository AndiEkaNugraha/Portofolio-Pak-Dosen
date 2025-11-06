# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Daftar Acara Dosen',
    'version': '1.0.6',
    'summary': 'Daftar Acara yang Diisi Dosen',
    'description': """
Portfolio Acara Dosen
=====================
Module untuk mengelola portfolio acara yang diisi oleh dosen seperti:
- Penyuluhan & Webinar
- Workshop & Pelatihan
- Seminar & Konferensi  
- Juri & Penilai
- Dan kegiatan lainnya

Fitur:
------
* Manajemen acara dengan detail lengkap
* Kategori & jenis acara
* Format acara (offline/online/hybrid)
* Dokumentasi (sertifikat, presentasi, foto)
* Evaluasi & impact tracking
* Website portfolio dengan filter
* SEO-friendly URLs
* Responsive design
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/acara_data.xml',
        'views/acara_views.xml',
        'templates/acara_templates.xml',
        'views/acara_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}