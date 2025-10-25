# Plugin Produk Penelitian untuk Odoo 19

Plugin ini dibuat untuk mengelola dan menampilkan produk-produk hasil penelitian di lingkungan akademik atau lembaga penelitian. Plugin ini menggunakan plugin `hki_paten` sebagai acuan struktur dan konsep yang baik.

## Fitur Utama

### 1. Manajemen Produk Penelitian
- **Kategori Produk**: Pengelompokan berdasarkan bidang teknologi, aplikasi, dan disiplin ilmu
- **Tipe Produk**: Pembedaan antara prototype dan produk jadi
- **Status Pengembangan**: Tracking tahapan dari konsep hingga komersialisasi
- **Technology Readiness Level (TRL)**: Penilaian kematangan teknologi (1-9)

### 2. Informasi Komprehensif
- **Detail Teknis**: Spesifikasi lengkap, requirements, dan arsitektur
- **Tim Peneliti**: Data peneliti utama dan tim riset
- **Aspek Komersial**: Potensi pasar, keunggulan kompetitif, estimasi biaya
- **Kekayaan Intelektual**: Status paten, trademark, dan lisensi
- **Regulasi**: Compliance dan sertifikasi yang diperlukan

### 3. Website Frontend
- **Halaman Publik**: Showcase produk penelitian untuk publik
- **Filter & Pencarian**: Berdasarkan kategori, tipe, status, TRL
- **Detail Produk**: Informasi lengkap dengan kontak peneliti
- **Responsive Design**: Bootstrap 5 untuk tampilan modern

### 4. Backend Management
- **Form Views**: Input data lengkap dengan notebook tabs
- **List Views**: Overview produk dengan status indicators  
- **Kanban Views**: Visual management dengan gambar
- **Search & Filter**: Tools pencarian dan filtering canggih

## Struktur Data

### Model Utama

#### 1. `produk.blog` (Kategori)
- `name`: Nama kategori
- `description`: Deskripsi kategori
- `technology_focus`: Fokus teknologi (AI, IoT, Biotech, dll)
- `application_area`: Area aplikasi (Healthcare, Education, dll)
- `scientific_field`: Bidang ilmiah (Computer Science, Engineering, dll)

#### 2. `produk.post` (Produk Penelitian)
**Informasi Umum:**
- `name`: Nama produk
- `subtitle`: Subtitle/tagline
- `description`: Deskripsi lengkap
- `blog_id`: Kategori produk
- `tag_ids`: Tags untuk pencarian

**Klasifikasi:**
- `product_type`: prototype/product
- `product_category`: innovation/applied_research/basic_research
- `development_status`: concept/development/testing/pilot_project/commercialization/completed
- `trl_level`: Technology Readiness Level (1-9)

**Detail Teknis:**
- `technical_specs`: Spesifikasi teknis
- `system_requirements`: Requirements sistem
- `technical_architecture`: Arsitektur teknis
- `performance_metrics`: Metrik performa

**Tim & Penelitian:**
- `main_researcher`: Peneliti utama
- `research_team`: Tim peneliti
- `research_institution`: Institusi peneliti
- `funding_source`: Sumber pendanaan
- `research_duration`: Durasi penelitian

**Aspek Komersial:**
- `estimated_cost`: Estimasi biaya pengembangan
- `development_duration`: Durasi pengembangan (bulan)
- `target_market`: Target pasar
- `competitive_advantage`: Keunggulan kompetitif
- `market_size`: Ukuran pasar
- `revenue_model`: Model bisnis
- `commercial_potential`: Potensi komersial

**Kekayaan Intelektual:**
- `intellectual_property`: Status IP
- `patent_status`: Status paten
- `trademark_info`: Informasi trademark
- `licensing_terms`: Syarat lisensi

**Regulasi & Compliance:**  
- `regulatory_status`: Status regulasi
- `certification_needed`: Sertifikasi yang diperlukan
- `compliance_standards`: Standar compliance

**Media & Dokumentasi:**
- `image_1920`: Gambar utama produk
- `documentation_url`: URL dokumentasi
- `demo_url`: URL demo
- `video_url`: URL video
- `presentation_url`: URL presentasi

#### 3. Helper Models
- `produk.type`: Master data tipe produk
- `produk.technology`: Master data teknologi

## Instalasi

1. Copy folder `produk_penelitian` ke direktori `addons/`
2. Restart Odoo server
3. Aktifkan Developer Mode
4. Go to Apps → Update Apps List
5. Search "Produk Penelitian" dan install
6. Module akan otomatis membuat data default dan demo

## Penggunaan

### Backend (Admin)
1. Go to **Produk Penelitian** menu
2. Manage **Kategori** untuk pengelompokan
3. Create **Produk** baru dengan data lengkap
4. Use **Konfigurasi** untuk setup tipe dan teknologi

### Frontend (Website)
1. Visit `/produk-penelitian` untuk halaman utama
2. Browse by kategori atau gunakan filter
3. Click produk untuk detail lengkap
4. Use contact form untuk inquiry

## Kustomisasi

### Menambah Field Baru
Edit file `models/produk_post.py` dan tambah field:
```python
new_field = fields.Char('New Field')
```

### Menambah View
Edit file `views/produk_views.xml` dan tambah field ke form view:
```xml
<field name="new_field"/>
```

### Styling Template
Edit file `templates/produk_templates.xml` untuk kustomisasi tampilan.

## Kompatibilitas

- **Odoo Version**: 19.0+
- **Python**: 3.8+
- **Dependencies**: 
  - base
  - website  
  - mail
  - portal (optional)
  - crm (optional untuk lead generation)

## Teknologi

- **Framework**: Odoo 19 (modern architecture)
- **Backend**: Python dengan ORM Odoo
- **Frontend**: Bootstrap 5, modern HTML5/CSS3
- **Views**: Menggunakan 'list' view (bukan deprecated 'tree')
- **Widgets**: Modern statusbar, notebook, kanban
- **API**: JSON endpoints untuk AJAX interactions

## Struktur File

```
produk_penelitian/
├── __init__.py
├── __manifest__.py
├── README.md
├── controllers/
│   ├── __init__.py
│   └── main.py
├── data/
│   └── produk_data.xml
├── demo/
│   └── produk_demo.xml  
├── models/
│   ├── __init__.py
│   ├── produk_blog.py
│   └── produk_post.py
├── security/
│   └── ir.model.access.csv
├── static/
│   └── description/
│       └── icon.png
├── templates/
│   └── produk_templates.xml
└── views/
    ├── produk_menus.xml
    └── produk_views.xml
```

## Roadmap

### Phase 1 (Current)
- ✅ Basic CRUD operations
- ✅ Website frontend  
- ✅ Search & filtering
- ✅ TRL tracking

### Phase 2 (Future)
- [ ] Advanced reporting & analytics
- [ ] Integration dengan sistem akademik
- [ ] Export to various formats
- [ ] Advanced workflow management
- [ ] Multi-language support
- [ ] API endpoints untuk integrasi

### Phase 3 (Future)
- [ ] Mobile app companion
- [ ] AI-powered recommendations
- [ ] Collaboration tools
- [ ] Advanced project management

## Support

Untuk pertanyaan atau issue:
1. Check dokumentasi Odoo 19
2. Review kode plugin `hki_paten` sebagai referensi
3. Test dengan data demo yang disediakan

## Lisensi

LGPL-3 (mengikuti lisensi Odoo)

---

Plugin ini dikembangkan menggunakan best practices Odoo 19 dan mengacu pada struktur plugin `hki_paten` yang sudah terbukti baik dan sesuai.