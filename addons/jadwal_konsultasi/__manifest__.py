# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Jadwal Konsultasi Mahasiswa',
    'version': '1.0.0',
    'summary': 'Manajemen Jadwal dan Jam Konsultasi Dosen untuk Mahasiswa',
    'description': """
        Modul untuk mengelola jadwal dan jam konsultasi dosen dengan fitur:
        - Daftar jadwal konsultasi dengan hari dan jam
        - Lokasi konsultasi (ruangan, online, hybrid)
        - Jenis konsultasi (akademik, penelitian, skripsi, karir)
        - Kapasitas maksimal per slot konsultasi
        - Catatan dan deskripsi khusus
        - Status aktif/nonaktif jadwal
        - Tampilan kalender di website untuk mahasiswa
        - SEO optimization untuk halaman konsultasi
        - Notifikasi perubahan jadwal
        - Riwayat dan tracking konsultasi
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': ['base', 'website', 'mail', 'calendar'],
    'data': [
        'views/jadwal_konsultasi_views.xml',
        'views/jadwal_konsultasi_menus.xml',
        'data/jadwal_konsultasi_data.xml',
        'data/website_data.xml',
        'templates/jadwal_konsultasi_templates.xml',
    ],
    'external_dependencies': {
        'python': [],
    },
    'demo': [
        'data/jadwal_konsultasi_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
