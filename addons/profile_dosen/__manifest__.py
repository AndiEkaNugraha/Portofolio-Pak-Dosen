# -*- coding: utf-8 -*-
{
    'name': 'Portofolio Dosen - Profile Lengkap',
    'version': '1.0.0',
    'summary': 'Profile Lengkap Dosen dengan CV Generator',
    'description': """
        Modul untuk mengelola profile lengkap dosen meliputi:
        - Biografi lengkap
        - Riwayat pendidikan
        - Bidang keahlian & minat riset
        - Riwayat pekerjaan/jabatan
        - Daftar penghargaan & pengakuan
        - Generate CV ATS dari semua karya dosen
        
        CV Generator akan mengambil data dari:
        - Profile dosen (biografi, pendidikan, pekerjaan)
        - Jurnal ilmiah
        - Buku karya
        - HKI/Paten
        - Proyek penelitian
        - Pengabdian masyarakat
        - Prosiding konferensi
        - Hibah pendanaan
        - Produk penelitian
        - Aktivitas reviewer
        - Acara dosen
        - Grup riset
        - Mata kuliah
    """,
    'category': 'Website/Website',
    'author': 'Andi Eka Nugraha',
    'depends': [
        'base', 
        'website', 
        'website_blog', 
        'mail',
        # Dependencies untuk CV Generator
        'jurnal_ilmiah',
        'buku_karya',
        'hki_paten',
        'proyek_penelitian',
        'pengabdian_masyarakat',
        'prosiding_konferensi',
        'hibah_pendanaan',
        'produk_penelitian',
        'reviewer_dosen',
        'acara_dosen',
        'grup_riset',
        'mata_kuliah',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/profile_data.xml',
        'views/profile_views.xml',
        # 'templates/profile_templates.xml',  # File lama - disabled karena rusak
        'templates/profile_templates_sinta.xml',  # File baru dengan tab system
        # 'templates/cv_templates.xml',  # Tidak dipakai lagi, gunakan custom HTML di form
        'views/profile_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
