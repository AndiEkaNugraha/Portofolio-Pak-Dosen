# Modul Mata Kuliah (Matakuliah) - Odoo 19

Modul untuk mengelola dan mempublikasikan daftar mata kuliah yang diampu di website portofolio dosen.

## 📋 Fitur

### Backend (Management)
- ✅ **Kategori Mata Kuliah** - Organisir mata kuliah berdasarkan program studi dan semester
- ✅ **Informasi Lengkap** - Kode, nama, SKS, tipe (teori/praktik/seminar), status (wajib/pilihan)
- ✅ **Tujuan Pembelajaran** - TPU, Learning Outcomes, CPMK
- ✅ **Konten Silabus** - Deskripsi, silabus, materi detail, garis besar
- ✅ **Metode Pembelajaran** - Strategi, media, dan metode pengajaran
- ✅ **Penilaian** - Metode, komponen, skala penilaian, nilai minimum
- ✅ **Referensi** - Buku wajib, tambahan, sumber online, platform LMS
- ✅ **Jadwal Kelas** - Hari, jam, ruang, kapasitas, lokasi
- ✅ **Kontak Dosen** - Email, telepon, jam konsultasi, metode konsultasi
- ✅ **Asisten Dosen** - Info asisten dan kontak
- ✅ **Kebijakan** - Kehadiran, plagiarisme, tata tertib, ujian susulan
- ✅ **Upload Silabus** - File silabus dalam format PDF/DOC

### Website (Public Display)
- 🌐 **Halaman Daftar** - Grid view semua mata kuliah dengan filter
- 🌐 **Halaman Detail** - Tampilan lengkap dengan tab (Gambaran, Pembelajaran, Konten, Penilaian, Informasi)
- 🌐 **Pencarian** - Search mata kuliah berdasarkan kode atau nama
- 🌐 **Filter** - Filter by tipe (teori/praktik/seminar)
- 🌐 **Related Courses** - Rekomendasi mata kuliah terkait
- 🌐 **Download Silabus** - Direct download file silabus
- 🌐 **Sharing** - Share ke social media atau email
- 🌐 **SEO Optimization** - Meta tags, keywords, Open Graph image

## 🏗️ Arsitektur

Plugin ini mengikuti pola Blog Model Inheritance dari Odoo:

```
matakuliah.blog ────────────► (inherits blog.blog)
    │
    ├─ Kategori/Program
    ├─ Program studi
    └─ Jenis Program

matakuliah.post ────────────► (inherits blog.post)
    │
    ├─ Informasi dasar
    ├─ Tujuan pembelajaran
    ├─ Konten & silabus
    ├─ Penilaian
    ├─ Jadwal & lokasi
    ├─ Kontak dosen
    └─ SEO fields
```

## 📁 Struktur File

```
matakuliah/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── matakuliah_blog.py      # Kategori mata kuliah
│   └── matakuliah_post.py      # Detail mata kuliah (60+ fields)
├── controllers/
│   ├── __init__.py
│   └── main.py                 # 5 routes website
├── views/
│   ├── matakuliah_views.xml    # Backend forms & list views
│   └── matakuliah_menus.xml    # Menu structure
├── templates/
│   └── matakuliah_templates.xml # Website HTML templates
├── security/
│   └── ir.model.access.csv     # Access control rules
└── data/
    └── matakuliah_data.xml     # Sample data & categories
```

## 🔌 Instalasi

### 1. Copy ke Addon Folder
```bash
cp -r matakuliah /path/to/odoo/addons/
```

### 2. Update Apps List
- Buka Odoo
- Navigasi ke Apps
- Click "Update Apps List"

### 3. Install Modul
- Search "Mata Kuliah"
- Click Install

### 4. Verifikasi
Setelah install berhasil, menu "Mata Kuliah" akan muncul di sidebar.

## 🚀 Penggunaan

### Membuat Kategori Program Studi
1. Buka Menu: **Mata Kuliah → Kategori/Program**
2. Click "Create"
3. Isi:
   - Nama Program (e.g., "Teknik Pemrograman")
   - Program Studi (e.g., "Teknik Informatika")
   - Jenis Program
   - Deskripsi (optional)
4. Click "Save"

### Membuat Mata Kuliah
1. Buka Menu: **Mata Kuliah → Daftar Mata Kuliah**
2. Click "Create"
3. Isi informasi di 10 tab:
   - **Informasi Dasar**: Kode, nama, SKS, tipe
   - **Tujuan & Pembelajaran**: TPU, outcomes, metode
   - **Konten & Silabus**: Deskripsi, silabus, upload file
   - **Penilaian**: Metode dan komponen penilaian
   - **Referensi**: Buku dan sumber online
   - **Jadwal Kelas**: Hari, jam, ruang, kapasitas
   - **Kontak Dosen**: Email, telepon, jam konsultasi
   - **Kebijakan**: Aturan kelas
   - **SEO & Website**: Meta tags, slug, publikasi
   - **Informasi Tambahan**: Data lainnya
4. Click "Publish" untuk mempublikasikan di website

## 🌐 URL Routes

| Route | Deskripsi | Auth |
|-------|-----------|------|
| `/mata-kuliah` | Halaman daftar semua mata kuliah | Public |
| `/mata-kuliah/<slug>` | Halaman detail mata kuliah | Public |
| `/mata-kuliah/search?q=keyword` | Pencarian mata kuliah | Public |
| `/mata-kuliah/by-type/<type>` | Filter by tipe (teori/praktik/seminar) | Public |
| `/mata-kuliah/<slug>/download-silabus` | Download file silabus | Public |

## 🔐 Keamanan

Akses diatur melalui `security/ir.model.access.csv`:

| Role | matakuliah.blog | matakuliah.post |
|------|---|---|
| User | Read | Read |
| Manager | CRUD | CRUD |

Website display bersifat **public** untuk semua user.

## 🎨 Customization

### Mengubah Template Website
Edit `templates/matakuliah_templates.xml`:
- `matakuliah_list_template` - Halaman daftar
- `matakuliah_detail_template` - Halaman detail

### Menambah Field Baru
1. Edit `models/matakuliah_post.py`
2. Tambah field dengan `fields.Char()`, `fields.Html()`, dll
3. Update form di `views/matakuliah_views.xml`
4. Update templates jika perlu

### Mengubah Menu
Edit `views/matakuliah_menus.xml` untuk mengubah struktur menu.

## 📊 Fields Reference

### matakuliah_post (Mata Kuliah)

#### Basic Information (5 fields)
- `course_code` - Kode mata kuliah (unique)
- `course_name` - Nama mata kuliah
- `course_english_name` - Nama dalam bahasa inggris
- `credits` - SKS (default 3)
- `course_type` - Tipe (teori/praktik/seminar/praktek_lapangan/tugas_akhir)

#### Requirements (4 fields)
- `prerequisites` - Prasyarat mata kuliah
- `corequisites` - Co-requisite
- `semester_offered` - Semester ditawarkan
- `status_course` - Status (wajib/pilihan/wajib_minat)

#### Learning (6 fields)
- `course_objectives` - Tujuan pembelajaran umum (TPU)
- `learning_outcomes` - Capaian pembelajaran
- `cpmk_text` - CPMK (Capaian Pembelajaran Mata Kuliah)
- `learning_methods` - Metode pembelajaran
- `teaching_strategy` - Strategi pengajaran
- `media_pembelajaran` - Media pembelajaran

#### Content (5 fields)
- `course_description` - Deskripsi mata kuliah
- `course_content` - Silabus lengkap
- `topics_outline` - Garis besar materi
- `detailed_content` - Materi detail/slide
- `course_syllabus_file` - Upload file silabus

#### Assessment (4 fields)
- `assessment_methods` - Metode penilaian
- `assessment_components` - Komponen penilaian
- `grading_scale` - Skala penilaian
- `minimum_grade` - Nilai minimum (A/B/C/D)

#### References (4 fields)
- `required_textbooks` - Buku referensi wajib
- `recommended_books` - Buku referensi tambahan
- `online_resources` - Sumber daya online
- `learning_platform` - Platform/LMS
- `course_website` - Website mata kuliah

#### Schedule (6 fields)
- `day_of_week` - Hari (monday-sunday)
- `start_time` - Jam mulai
- `end_time` - Jam berakhir
- `classroom` - Ruang kelas
- `building` - Gedung
- `capacity` - Kapasitas kelas
- `max_participants` - Maksimal peserta

#### Instructor Contact (4 fields)
- `instructor_email` - Email instruktur
- `instructor_phone` - Telepon instruktur
- `office_location` - Lokasi kantor
- `office_hours` - Jam konsultasi
- `consultation_methods` - Metode konsultasi

#### Teaching Assistants (2 fields)
- `teaching_assistants` - Data asisten dosen
- `ta_contact_info` - Kontak asisten

#### Policies (4 fields)
- `attendance_policy` - Kebijakan kehadiran
- `plagiarism_policy` - Kebijakan plagiarisme
- `classroom_policies` - Tata tertib kelas
- `makeup_policy` - Kebijakan ujian susulan

#### SEO Optimization (5 fields)
- `slug` - URL slug (unique, required)
- `meta_title` - Meta title (160 chars)
- `meta_description` - Meta description (160 chars)
- `meta_keywords` - Meta keywords
- `og_image` - Open Graph image

#### Additional (1 field)
- `additional_info` - Informasi tambahan

**Total: 60+ fields dalam 10 kategori**

## 🔧 Troubleshooting

### Module tidak muncul di Apps
- Jalankan "Update Apps List" di Settings
- Clear browser cache
- Restart Odoo service

### Error "slug must be unique"
- Setiap mata kuliah harus punya slug unik
- Slug auto-generate dari course_code jika tidak diisi

### Form tidak muncul dengan benar
- Clear browser cache (Ctrl+F5)
- Check console untuk error JavaScript
- Verifikasi XML views syntax

### Website tidak menampilkan mata kuliah
- Pastikan mata kuliah sudah di-publish (`website_published = True`)
- Check routing di controllers/main.py

## 📝 Database Constraints

```sql
UNIQUE(course_code)      -- Kode mata kuliah unik
UNIQUE(slug)             -- URL slug unik
```

## 🎓 Best Practices

1. **Kode Mata Kuliah**: Gunakan format standar (e.g., IF101, IF202)
2. **Slug**: Gunakan lowercase, hyphens, readable (e.g., pemrograman-python)
3. **Meta Tags**: Isi untuk SEO (max 160 chars)
4. **Silabus**: Upload file lengkap untuk referensi student
5. **Publish**: Jangan publish jika belum lengkap

## 📱 Responsive Design

Website template fully responsive:
- Desktop: 3 kolom grid
- Tablet: 2 kolom grid
- Mobile: 1 kolom grid

## 🔗 Dependencies

```
base
website
website_blog  ← Untuk blog inheritance
mail          ← Untuk notifikasi
```

## 👨‍💻 Developer Notes

### Model Inheritance
```python
class MatakuliahPost(models.Model):
    _name = 'matakuliah.post'
    _inherit = 'blog.post'  # Inherit dari blog.post Odoo
```

### Creating Slug
```python
def _generate_slug(self, text):
    import re
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')
```

### Controller Routing
```python
@http.route('/mata-kuliah', auth='public', website=True, sitemap=True)
def mata_kuliah_list(self, **kwargs):
    courses = request.env['matakuliah.post'].sudo().search([...])
    return request.render('matakuliah.matakuliah_list_template', {...})
```

## 📈 Version & Changelog

**v1.0.0** (Initial Release)
- Module creation berdasarkan Odoo 19
- 2 models (blog, post)
- 60+ fields di mata kuliah
- 2 website pages (list, detail)
- 5 routes
- Full SEO support
- Download silabus

## 📧 Support & Documentation

Untuk masalah teknis atau customization, silakan contact developer.

## 📄 License

LGPL-3 (Same as Odoo)

---

**Created for**: Portofolio Dosen Odoo 19
**Compatibility**: Odoo 19.0+
**Last Updated**: 2024
