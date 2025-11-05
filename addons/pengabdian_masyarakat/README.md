# Plugin Pengabdian Masyarakat untuk Odoo 19

Plugin untuk mengelola dan mempublikasikan kegiatan pengabdian masyarakat dalam website portofolio dosen.

## 📋 Analisis Plugin HKI & Paten

Berdasarkan analisis plugin `hki_paten`, saya mengidentifikasi konsep dan pola implementasi:

### Pola Arsitektur yang Diikuti:
1. **Inherit Model Blog** - Menggunakan `blog.blog` dan `blog.post` sebagai base model
2. **View Backend Terpisah** - Tidak inherit view, membuat form/tree/search sendiri  
3. **Controller Website Khusus** - Route `/pengabdian` terpisah dari blog standard
4. **Template Website Custom** - Template khusus untuk tampilan website
5. **SEO Optimization** - Meta tags, friendly URLs, structured content

### Field Khusus HKI:
- Detail pendaftaran (nomor, tanggal, kantor)
- Klasifikasi (IPC, Nice, Locarno)
- Status tracking (draft→registered)
- Protection period & expiry

## 🎯 Implementasi Plugin Pengabdian Masyarakat

Mengikuti pola yang sama dengan adaptasi untuk kegiatan pengabdian masyarakat:

### 1. Model Structure

#### `pengabdian.blog` (inherit `blog.blog`)
```python
- name: Nama Kategori Pengabdian
- pengabdian_scope: local/regional/national/international
- funding_source: internal/external/community/mixed
- service_field: education/health/agriculture/technology/economy/social/culture/other
```

#### `pengabdian.post` (inherit `blog.post`)
```python
- name: Judul Kegiatan Pengabdian
- pengabdian_type: pendidikan/kesehatan/pertanian/teknologi/sosial
- coordinator: Koordinator Kegiatan
- team_members: Anggota Tim
- implementation_date: Tanggal Pelaksanaan
- location: Lokasi Pelaksanaan
- target_participants: Target Peserta
- status: planned/ongoing/completed/reported
- total_budget: Total Anggaran
- funding_source_id: Sumber Pendanaan
- objectives: Tujuan Kegiatan
- results_achieved: Hasil yang Dicapai
- impact_assessment: Penilaian Dampak
- beneficiaries_count: Jumlah Penerima Manfaat
```

### 2. Controller Website

Route khusus `/pengabdian` dengan fitur:
- **Index**: `/pengabdian` - Daftar kegiatan dengan filter
- **Detail**: `/pengabdian/detail/{slug}-{id}` - Detail kegiatan
- **Category**: `/pengabdian/kategori/{id}` - Per kategori
- **Search**: `/pengabdian/search` - Pencarian lanjutan (future)

### 3. Template Website

Template responsive dengan:
- Grid layout untuk daftar kegiatan
- Card design dengan badges (jenis, status)
- Filter multi-criteria (jenis, kategori, tahun)
- Detail page dengan sidebar info lengkap
- SEO meta tags otomatis

### 4. Backend Views

- **Form View**: Input data kegiatan dengan notebook tabs
- **Tree View**: Daftar dengan kolom penting
- **Search View**: Filter dan group by

### 5. Menu Structure

```
Pengabdian Masyarakat
├── Daftar Kegiatan Pengabdian
├── Kategori Pengabdian
├── Berdasar Jenis
│   ├── Pengabdian Pendidikan
│   ├── Pengabdian Kesehatan
│   ├── Pengabdian Pertanian
│   └── Pengabdian Teknologi
└── Konfigurasi
    ├── Jenis Pengabdian
    └── Sumber Pendanaan
```

## 🚀 Instalasi

1. Copy folder `pengabdian_masyarakat` ke direktori `addons/`
2. Restart Odoo server
3. Update Apps List
4. Install module "Daftar Kegiatan Pengabdian"

## 📱 Penggunaan

### Backend:
1. Buka menu **Pengabdian Masyarakat**
2. Buat **Kategori Pengabdian** terlebih dahulu
3. Tambah **Kegiatan Pengabdian** dengan data lengkap
4. Set status ke "completed" atau "reported" untuk publish

### Website:
1. Akses `/pengabdian` untuk melihat daftar
2. Gunakan filter untuk pencarian spesifik
3. Klik detail untuk informasi lengkap

## 🎨 Fitur Website

### Halaman Utama `/pengabdian`
- Grid responsive dengan cards kegiatan
- Filter: kategori, jenis pengabdian, tahun
- Search box untuk pencarian teks
- Statistik dashboard

### Detail Kegiatan `/pengabdian/detail/{slug}-{id}`
- Layout 2 kolom dengan content & sidebar
- Breadcrumb navigation
- Related posts berdasar kategori
- Meta tags SEO otomatis

### Fitur Filter & Search
- Multi-select filters
- Advanced search form
- URL parameters maintained
- Real-time results

## 📊 Jenis Pengabdian yang Didukung

1. **Pengabdian Pendidikan** - Pelatihan, workshop, pengembangan kurikulum
2. **Pengabdian Kesehatan** - Penyuluhan kesehatan, pelayanan medis
3. **Pengabdian Pertanian** - Pelatihan pertanian, pengembangan teknologi
4. **Pengabdian Teknologi** - Literasi digital, pengembangan aplikasi
5. **Pengabdian Sosial** - Pemberdayaan masyarakat, pengentasan kemiskinan

## 🌐 Cakupan Kegiatan

- **Lokal** - Kegiatan di tingkat desa/kelurahan
- **Regional** - Kegiatan di tingkat kabupaten/kota
- **Nasional** - Kegiatan di tingkat nasional
- **Internasional** - Kegiatan lintas negara

## 💰 Sumber Pendanaan

- **Dana Internal** - Dari universitas/fakultas
- **Dana Eksternal** - Dari pemerintah/swasta/lembaga internasional
- **Dana Masyarakat** - Swadaya masyarakat
- **Campuran** - Kombinasi berbagai sumber

## 📈 Status Tracking

1. **Direncanakan** - Tahap perencanaan dan proposal
2. **Sedang Berlangsung** - Kegiatan dalam pelaksanaan
3. **Selesai** - Kegiatan telah selesai dilaksanakan
4. **Telah Dilaporkan** - Laporan akhir telah disubmit

## 🔧 Kustomisasi

### Tambah Field Custom
Edit `models/pengabdian_post.py` dan tambah field baru:

```python
custom_field = fields.Char('Custom Field')
```

### Modify Template
Edit `templates/pengabdian_templates.xml` untuk mengubah tampilan website.

### Add New Pengabdian Type
Tambah option di selection field `pengabdian_type` dalam model.

## 📋 Demo Data

Plugin include demo data:
- 2 kategori pengabdian (Pendidikan, Kesehatan)
- 4 jenis pengabdian
- 3 sumber pendanaan
- 1 sample kegiatan dengan data lengkap

## 🎯 Perbedaan dengan Plugin HKI

| Aspek | HKI & Paten | Pengabdian Masyarakat |
|-------|-------------|----------------------|
| **Focus** | Intellectual Property | Community Service |
| **Main Entity** | IP Registration | Community Activity |
| **Key Dates** | Application/Registration | Implementation/Completion |
| **Classification** | IPC/Nice/Locarno | Service Field/Type |
| **Status** | Draft→Registered | Planned→Reported |
| **Impact** | Legal Protection | Social Impact |

## ✅ Checklist Implementasi

- [x] Model `pengabdian.blog` inherit dari `blog.blog`
- [x] Model `pengabdian.post` inherit dari `blog.post`
- [x] Controller dengan route `/pengabdian/*`
- [x] Template website responsive
- [x] Backend views (form/tree)
- [x] Menu structure lengkap
- [x] Security access rules
- [x] Demo data & categories
- [x] SEO optimization
- [x] Documentation lengkap

## 🚀 Next Steps

1. **Test Installation** - Install dan test semua fitur
2. **Add Custom CSS** - Sesuaikan styling dengan theme website
3. **Extend Fields** - Tambah field spesifik kebutuhan
4. **Add Reporting** - Buat report PDF untuk laporan kegiatan
5. **Impact Dashboard** - Dashboard visual untuk metrik dampak

---

**Developed for Odoo 19** | Compatible dengan Community & Enterprise Edition