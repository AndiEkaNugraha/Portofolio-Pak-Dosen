# Plugin HKI & Paten untuk Odoo 19

Plugin untuk mengelola dan mempublikasikan Hak Kekayaan Intelektual & Paten dalam website portofolio dosen.

## 📋 Analisis Plugin Prosiding Konferensi

Berdasarkan analisis plugin `prosiding_konferensi`, saya mengidentifikasi konsep dan pola implementasi:

### Pola Arsitektur yang Diikuti:
1. **Inherit Model Blog** - Menggunakan `blog.blog` dan `blog.post` sebagai base model
2. **View Backend Terpisah** - Tidak inherit view, membuat form/tree/search sendiri  
3. **Controller Website Khusus** - Route `/prosiding` terpisah dari blog standard
4. **Template Website Custom** - Template khusus untuk tampilan website
5. **SEO Optimization** - Meta tags, friendly URLs, structured content

### Field Khusus Prosiding:
- Detail konferensi (nama, tanggal, lokasi, penyelenggara)
- Informasi publikasi (penerbit, volume, halaman, DOI)
- Klasifikasi (rank konferensi, indexing)
- SEO fields (slug, meta title/description)

## 🎯 Implementasi Plugin HKI & Paten

Mengikuti pola yang sama dengan adaptasi untuk HKI & Paten:

### 1. Model Structure

#### `hki.blog` (inherit `blog.blog`)
```python
- name: Nama Kategori HKI
- hki_scope: national/international/both
- registration_office: Kantor pendaftaran (Kemenkumham, USPTO, dll)
- scientific_field: Bidang keilmuan
```

#### `hki.post` (inherit `blog.post`) 
```python
- name: Judul HKI/Paten
- hki_type: copyright/patent/trademark/industrial_design/dll
- creators: Pencipta/Inventor
- applicant: Pemohon/Pemegang Hak
- application_date: Tanggal Permohonan
- registration_number: Nomor Pendaftaran
- status: draft/applied/under_examination/granted/registered
- protection_period: Masa Perlindungan
- technical_field: Bidang Teknik
- ipc_classification: Klasifikasi IPC
```

### 2. Controller Website

Route khusus `/hki` dengan fitur:
- **Index**: `/hki` - Daftar HKI dengan filter
- **Detail**: `/hki/detail/{slug}-{id}` - Detail HKI
- **Category**: `/hki/kategori/{id}` - Per kategori
- **Search**: `/hki/search` - Pencarian lanjutan
- **Statistics**: `/hki/statistik` - Dashboard statistik

### 3. Template Website

Template responsive dengan:
- Grid layout untuk daftar HKI
- Card design dengan badges (jenis, status)
- Filter multi-criteria (jenis, tahun, kantor, status)
- Detail page dengan sidebar info
- SEO meta tags otomatis

### 4. Backend Views

- **Form View**: Input data HKI dengan notebook tabs
- **Tree View**: Daftar dengan kolom penting
- **Search View**: Filter dan group by
- **Kanban View**: Card view untuk mobile

### 5. Menu Structure

```
HKI & Paten
├── Daftar HKI & Paten
├── Kategori HKI
├── Berdasar Jenis
│   ├── Hak Cipta
│   ├── Paten  
│   ├── Merek
│   └── Desain Industri
└── Statistik
```

## 🚀 Instalasi

1. Copy folder `hki_paten` ke direktori `addons/`
2. Restart Odoo server
3. Update Apps List
4. Install module "Daftar HKI & Paten"

## 📱 Penggunaan

### Backend:
1. Buka menu **HKI & Paten** 
2. Buat **Kategori HKI** terlebih dahulu
3. Tambah **HKI & Paten** dengan data lengkap
4. Set status ke "registered" atau "granted" untuk publish

### Website:
1. Akses `/hki` untuk melihat daftar
2. Gunakan filter untuk pencarian spesifik
3. Klik detail untuk informasi lengkap

## 🎨 Fitur Website

### Halaman Utama `/hki`
- Grid responsive dengan cards HKI
- Filter: kategori, jenis HKI, tahun, kantor
- Search box untuk pencarian teks
- Pagination otomatis

### Detail HKI `/hki/detail/{slug}-{id}`
- Layout 2 kolom dengan content & sidebar
- Breadcrumb navigation
- Related posts berdasar kategori
- Meta tags SEO otomatis

### Fitur Filter & Search
- Multi-select filters
- Advanced search form
- URL parameters maintained
- Real-time results

## 📊 Jenis HKI yang Didukung

1. **Hak Cipta** - Karya tulis, program, seni
2. **Paten** - Penemuan teknologi  
3. **Paten Sederhana** - Penemuan sederhana
4. **Merek** - Tanda pengenal produk/jasa
5. **Desain Industri** - Desain produk
6. **Desain Tata Letak** - IC layout
7. **Varietas Tanaman** - Varietas baru tanaman
8. **Rahasia Dagang** - Trade secret

## 🌐 Kantor Pendaftaran

- **Kemenkumham RI** - Indonesia
- **USPTO** - Amerika Serikat  
- **EPO** - Eropa
- **JPO** - Jepang
- **KIPO** - Korea
- **SIPO** - China
- **WIPO** - World Intellectual Property

## 📈 Status Tracking

1. **Draft** - Persiapan dokumen
2. **Applied** - Diajukan  
3. **Under Examination** - Dalam pemeriksaan
4. **Published** - Dipublikasi
5. **Granted** - Diberikan
6. **Registered** - Terdaftar
7. **Rejected** - Ditolak
8. **Expired** - Berakhir

## 🔧 Kustomisasi

### Tambah Field Custom
Edit `models/hki_post.py` dan tambah field baru:

```python
custom_field = fields.Char('Custom Field')
```

### Modify Template
Edit `templates/hki_templates.xml` untuk mengubah tampilan website.

### Add New HKI Type
Tambah option di selection field `hki_type` dalam model.

## 📋 Demo Data

Plugin include demo data:
- 4 kategori HKI (Hak Cipta, Paten, Merek, Desain)
- 4 sample HKI posts dengan data lengkap
- Website menu otomatis

## 🎯 Perbedaan dengan Plugin Prosiding

| Aspek | Prosiding Konferensi | HKI & Paten |
|-------|---------------------|-------------|
| **Focus** | Paper & Conference | Intellectual Property |
| **Main Entity** | Conference Paper | IP Registration |  
| **Key Dates** | Conference Date | Application/Registration Date |
| **Classification** | Conference Rank/Indexing | IPC/Nice/Locarno Classification |
| **Status** | Published/Accepted | Draft→Registered |
| **Protection** | Citation Impact | Legal Protection Period |

## ✅ Checklist Implementasi

- [x] Model `hki.blog` inherit dari `blog.blog`
- [x] Model `hki.post` inherit dari `blog.post`  
- [x] Controller dengan route `/hki/*`
- [x] Template website responsive
- [x] Backend views (form/tree/search/kanban)
- [x] Menu structure lengkap
- [x] Security access rules
- [x] Demo data & categories
- [x] SEO optimization
- [x] Documentation lengkap

## 🚀 Next Steps

1. **Test Installation** - Install dan test semua fitur
2. **Add Custom CSS** - Sesuaikan styling dengan theme website
3. **Extend Fields** - Tambah field spesifik kebutuhan
4. **Add Reporting** - Buat report PDF untuk sertifikat
5. **API Integration** - Integrasi dengan database HKI eksternal

---

**Developed for Odoo 19** | Compatible dengan Community & Enterprise Edition