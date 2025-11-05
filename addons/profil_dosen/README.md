# Profil Dosen Module

Modul untuk mengelola halaman profil lengkap dosen di Odoo 19.

## Fitur

- **Biografi Lengkap**: Deskripsi detail tentang dosen
- **Riwayat Pendidikan**: Mencatat semua jenjang pendidikan
- **Bidang Keahlian & Minat Riset**: Detail tentang keahlian dan area penelitian
- **Riwayat Pekerjaan/Jabatan**: Riwayat karir dan posisi sebelumnya
- **Penghargaan & Pengakuan**: Daftar penghargaan yang diterima
- **Download CV**: Fitur untuk download CV dosen
- **SEO Friendly**: Dengan slug, meta title, meta description, dan meta keywords
- **Responsive Design**: Website responsif untuk semua ukuran layar

## Struktur Data

### 1. Profil Blog (profil.blog)
Model untuk kategori profil dosen. Inherit dari `blog.blog`.

**Fields:**
- `name`: Nama kategori profil
- `subtitle`: Deskripsi singkat kategori
- `description`: Deskripsi lengkap kategori
- `dosen_category`: Kategori dosen (Akademik, Teknis, Profesional, Umum)

### 2. Profil Post (profil.post)
Model utama untuk data profil dosen.

**Fields Utama:**
- `name`: Nama dosen
- `blog_id`: Referensi ke kategori profil
- `image`: Foto profil
- `nip`: Nomor Induk Pegawai
- `email`: Email dosen
- `phone`: Nomor telepon
- `office`: Ruang kantor
- `biography`: Biografi lengkap (HTML)
- `expertise_fields`: Bidang keahlian (HTML)
- `research_interest`: Minat penelitian (HTML)
- `cv_file`: File CV (binary)
- `is_published`: Tampilkan di website

**SEO Fields:**
- `slug`: URL slug yang ramah (auto-generated)
- `meta_title`: Meta title untuk SEO
- `meta_description`: Meta description untuk SEO
- `meta_keywords`: Meta keywords untuk SEO

### 3. Profil Education (profil.education)
Riwayat pendidikan dosen.

**Fields:**
- `profil_post_id`: Referensi ke profil dosen
- `education_level`: Jenjang pendidikan (SMA, D3, S1, S2, S3, Post Doc, Lainnya)
- `institution`: Institusi/Universitas
- `field_of_study`: Program studi/bidang
- `start_year`: Tahun mulai
- `graduation_year`: Tahun lulus
- `gpa`: IPK/GPA
- `thesis_title`: Judul tesis/disertasi
- `advisor`: Dosen pembimbing

### 4. Profil Skill (profil.skill)
Bidang keahlian dan minat riset.

**Fields:**
- `profil_post_id`: Referensi ke profil dosen
- `name`: Nama keahlian
- `description`: Deskripsi keahlian
- `skill_type`: Jenis (Bidang Keahlian, Minat Riset, Spesialisasi, Kompetensi)
- `proficiency_level`: Tingkat keahlian (Pemula, Menengah, Mahir, Ahli)
- `is_primary`: Keahlian utama
- `years_of_experience`: Pengalaman (tahun)

### 5. Profil Experience (profil.experience)
Riwayat pekerjaan dan jabatan.

**Fields:**
- `profil_post_id`: Referensi ke profil dosen
- `job_title`: Posisi/Jabatan
- `organization`: Organisasi/Institusi
- `position_type`: Jenis posisi (Mengajar, Penelitian, Administrasi, Kepemimpinan, Konsultasi, Industri, Lainnya)
- `start_date`: Tanggal mulai
- `end_date`: Tanggal berakhir
- `is_current`: Posisi saat ini
- `description`: Deskripsi posisi (HTML)
- `location`: Lokasi
- `achievements`: Pencapaian/Kontribusi (HTML)

### 6. Profil Award (profil.award)
Penghargaan dan pengakuan.

**Fields:**
- `profil_post_id`: Referensi ke profil dosen
- `name`: Nama penghargaan
- `issuer`: Pemberi penghargaan
- `award_type`: Jenis penghargaan (Internasional, Nasional, Regional, Institusi, Pengakuan, Sertifikat, Lainnya)
- `award_date`: Tanggal penghargaan
- `description`: Deskripsi penghargaan (HTML)
- `importance`: Tingkat kepentingan
- `certificate_file`: File sertifikat
- `is_featured`: Tampilkan di highlight

## Routes/URLs

### Frontend Routes

- `/profil`: Halaman daftar profil dosen
- `/profil/page/<page>`: Halaman daftar dengan paginasi
- `/profil/<slug>`: Halaman detail profil dosen
- `/profil/<slug>/download-cv`: Download CV dosen

### Backend Routes (Menu)

- **Profil Dosen** (Main Menu)
  - Kategori Profil
  - Data Profil Dosen
  - Riwayat Pendidikan
  - Bidang Keahlian
  - Riwayat Pekerjaan
  - Penghargaan & Pengakuan

## Fitur SEO

1. **Slug URL**: Otomatis di-generate dari nama dosen
2. **Meta Title**: Judul khusus untuk SEO (default: nama dosen)
3. **Meta Description**: Deskripsi untuk search engine (default: ringkasan bio)
4. **Meta Keywords**: Kata kunci untuk SEO

## Template Website

### Halaman List (/profil)
- Pencarian berdasarkan nama, NIP, email, keahlian
- Filter berdasarkan kategori
- Statistik dosen
- Kartu profil dengan foto, nama, NIP, dan preview keahlian
- Pagination

### Halaman Detail (/profil/<slug>)
- Foto profil yang besar
- Informasi kontak lengkap
- Tombol download CV
- Biografi lengkap
- Keahlian & minat riset dengan daftar detail
- Timeline pendidikan
- Timeline pekerjaan/jabatan
- Daftar penghargaan & pengakuan
- Sidebar dengan info ringkas

## Styling & Design

- **Card-based Design**: Grid layout yang responsif
- **Timeline View**: Untuk riwayat pendidikan dan pekerjaan
- **Modern Colors**: Gradient dan warna yang menarik
- **Responsive**: Optimal di desktop, tablet, dan mobile
- **Smooth Animations**: Hover effects dan transitions

## Instalasi

1. Download/clone module ke direktori `addons`
2. Pergi ke **Apps** dan cari "Profil Dosen"
3. Klik **Install**

## Penggunaan

1. Pergi ke **Profil Dosen** menu
2. Buat kategori profil di **Kategori Profil**
3. Tambah profil dosen baru di **Data Profil Dosen**
4. Isi semua detail: biografi, pendidikan, keahlian, pekerjaan, penghargaan
5. Upload foto profil dan CV
6. Isi SEO fields (slug, meta title, meta description)
7. Centang **Tampilkan di Website** untuk publish
8. Profil akan muncul di `/profil` dan `/profil/<slug>`

## Security

- Hanya user yang di-publish yang muncul di website
- Access control via ir.model.access.csv
- Read/write/create/delete permissions per role

## Dependensi

- `base`
- `website`
- `website_blog`
- `mail`

## Versi

- **Versi**: 1.0.0
- **Kompatibel dengan**: Odoo 19
- **Lisensi**: LGPL-3

## Author

Andi Eka Nugraha

## TODO/Future Enhancements

- [ ] Import/export profil dosen
- [ ] Filter berdasarkan bidang keahlian
- [ ] Social media links
- [ ] Statistics dashboard
- [ ] Email notification pada publish
- [ ] Multi-language support enhancement
- [ ] Advanced search dengan filters lebih detail
