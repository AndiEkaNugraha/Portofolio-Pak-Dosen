# Panduan Modul Bimbingan Mahasiswa

## Overview
Modul `bimbingan_mahasiswa` adalah modul Odoo 17/19 untuk mengelola informasi bimbingan akademik mahasiswa di website portofolio dosen. Modul ini menyediakan:

- **Backend Management**: Form lengkap untuk mencatat data bimbingan
- **Website Display**: Tampilan responsif di halaman `/bimbingan-mahasiswa`
- **SEO Optimization**: Slug auto-generate, meta tags untuk SEO
- **Filtering & Search**: Filter berdasarkan jenis bimbingan, status
- **Progress Tracking**: Persentase penyelesaian, jumlah pertemuan, jam bimbingan

---

## File Structure

```
bimbingan_mahasiswa/
├── __init__.py                  # Package initializer
├── __manifest__.py              # Module metadata & dependencies
├── controllers/
│   ├── __init__.py
│   └── main.py                 # Website routes & logic
├── models/
│   ├── __init__.py
│   └── bimbingan_post.py       # ORM Model definition
├── views/
│   ├── bimbingan_views.xml     # Backend List/Form/Search views
│   └── bimbingan_menus.xml     # Backend menu items
├── templates/
│   └── bimbingan_templates.xml # Website frontend templates
├── data/
│   ├── bimbingan_data.xml      # Website menu + data
│   └── bimbingan_demo.xml      # Demo records (5 records)
├── security/
│   └── ir.model.access.csv     # Row-level access control
└── static/
    └── src/css/
        └── style.css           # Frontend styling
```

---

## Model Fields (bimbingan.mahasiswa)

### Basic Information
- **name** (Char, required): Judul bimbingan
- **subtitle** (Char): Sub judul/deskripsi singkat
- **description** (Html): Deskripsi lengkap bimbingan

### Student Information
- **student_name** (Char, required): Nama mahasiswa
- **student_id** (Char, required): NIM/NPM
- **student_email** (Char): Email mahasiswa
- **student_phone** (Char): Nomor telepon/WhatsApp
- **study_program** (Char, required): Program studi
- **academic_level** (Selection, required): S1/S2/S3

### Guidance Details
- **guidance_type** (Selection, required): thesis/project/research/academic/course/other
- **topic** (Char, required): Tema/topik bimbingan
- **guidance_output** (Selection): thesis/paper/prototype/publication/patent/other

### Schedule & Duration
- **guidance_date** (Date, required): Tanggal mulai bimbingan
- **estimated_completion** (Date): Target selesai
- **duration_months** (Integer): Durasi bimbingan (bulan)

### Status & Progress
- **status** (Selection): active/completed/on_hold/pending
- **completion_percentage** (Integer 0-100): Progress bimbingan
- **meeting_count** (Integer): Jumlah pertemuan
- **total_hours** (Integer): Total jam bimbingan
- **guidance_notes** (Html): Catatan/hasil bimbingan

### SEO Fields (Auto-generated)
- **slug** (Char, computed): URL slug (lowercase, regex cleaned)
- **meta_title** (Char): Meta title (auto-generated dari name jika kosong)
- **meta_description** (Char): Meta description (160 chars, auto-generated)
- **meta_keywords** (Char): Keywords untuk SEO

### Publishing
- **is_published** (Boolean): Manual publish toggle
- **website_published** (Related, readonly): Linked ke website.published.mixin

---

## Backend Usage

### Adding New Guidance Entry

1. **Go to Menu**: Bimbingan Mahasiswa → Daftar Bimbingan
2. **Click**: "Create" button
3. **Fill Required Fields**:
   - Judul Bimbingan
   - Nama Mahasiswa, NIM, Program Studi, Jenjang
   - Jenis Bimbingan, Tema/Topik
   - Tanggal Mulai Bimbingan
4. **Optional Fields** (Tab by tab):
   - **Detail Bimbingan**: Deskripsi lengkap, jadwal target, durasi
   - **Progress & Hasil**: Status, persentase, meeting count, jam bimbingan
   - **SEO**: Manual edit meta tags jika ingin (auto-generated jika kosong)
5. **Save & Publish**: Centang "Published" untuk tampil di website
6. **Status Buttons**: Gunakan buttons di header untuk ubah status (Mark as Completed, Active, Hold)

### Data Fields Explanation

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Judul Bimbingan | Text | Nama guidance yang jelas | "Sistem Informasi Manajemen Inventori" |
| Nama Mahasiswa | Text | Nama lengkap | "Budi Santoso" |
| NIM/NPM | Text | Nomor identitas | "20210001" |
| Tema/Topik | Text | Focus area | "Sistem Inventori berbasis Web" |
| Jenis Bimbingan | Selection | Kategori guidance | Thesis, Project, Research, etc |
| Status | Selection | Current state | Active, Completed, On Hold, Pending |
| Persentase Penyelesaian | % | Progress | 45%, 100%, dll |
| Jenis Output | Selection | Expected output | Thesis, Paper, Prototype, Patent, etc |

---

## Website Frontend

### Main Page: /bimbingan-mahasiswa

**Features:**
- Daftar semua guidance entries yang published
- Search by: name, topic, student name, program
- Filter by: guidance type, status
- Statistics card: Total count, Active count
- Card layout dengan status badge, progress bar
- Mobile responsive (1-4 columns)

**URL Parameters:**
```
/bimbingan-mahasiswa?guidance_type=thesis&status=active&search=sistem
```

### Detail Page: /bimbingan-mahasiswa/{slug}

**Layout:**
- Breadcrumb navigation
- Title & Subtitle
- Hero section dengan status, progress bar
- Main content (8 cols):
  - Student info section
  - Guidance details & description
  - Notes/hasil
  - Statistics (meetings, hours)
- Sidebar (4 cols):
  - Quick info card
  - Type/status/progress
  - Keywords/tags

---

## Demo Data

Module includes 5 demo records:

1. **Skripsi SI - Sistem Inventori**
   - Student: Budi Santoso (20210001)
   - Type: Thesis | Status: Active | Progress: 45%

2. **Tesis S2 - Cybersecurity**
   - Student: Siti Nurhaliza (20220045)
   - Type: Research | Status: Active | Progress: 60%

3. **Akademik - Algoritma**
   - Student: Andi Wijaya (20230015)
   - Type: Course | Status: Active | Progress: 30%

4. **Proyek Akhir - Mobile E-Learning**
   - Student: Dewi Putri (20230028)
   - Type: Project | Status: Active | Progress: 75%

5. **Skripsi Selesai - IoT Database**
   - Student: Roni Setiawan (20220010)
   - Type: Thesis | Status: Completed | Progress: 100%

---

## SEO & Meta Tags

### Auto-Generation Logic

**Slug Generation:**
```
Input: "Pengembangan Sistem Informasi Manajemen Inventori"
Output: "pengembangan-sistem-informasi-manajemen-inventori"
```
- Lowercase + regex cleaning (remove special chars)
- Replace spaces with dashes
- Auto-computed field

**Meta Title (if empty):**
```
auto-generated = name (first 60 chars)
Example: "Bimbingan Skripsi: Sistem Informasi..."
```

**Meta Description (if empty):**
```
auto-generated = subtitle + study_program + topic (max 160 chars)
Example: "Bimbingan Skripsi Mahasiswa Teknik Informatika. Sistem Informasi..."
```

**Meta Keywords (if empty):**
```
auto-generated = study_program + guidance_type + topic + "bimbingan mahasiswa"
Example: "teknik informatika, thesis, sistem informasi, bimbingan mahasiswa"
```

---

## Security & Access Control

### User Groups

| Group | Permission | Notes |
|-------|-----------|-------|
| Public | Read only published records | Via website frontend only |
| User (base.group_user) | Full CRUD | Can create/edit/delete own records |
| Admin (base.group_erp_manager) | Full CRUD + system | Can manage all records |

---

## Installation & Setup

### Prerequisites
- Odoo 17/19 installed
- website module activated
- mail module activated

### Install Module

1. **Method 1: Via Odoo UI**
   - Apps → "Modules" → "Update Modules List"
   - Search: "bimbingan_mahasiswa"
   - Click Install

2. **Method 2: Via Command Line**
   ```bash
   docker exec odoo_app odoo -u bimbingan_mahasiswa -d database_name
   ```

### Post-Installation

1. Go to **Bimbingan Mahasiswa → Daftar Bimbingan**
2. Verify 5 demo records appear
3. Visit `/bimbingan-mahasiswa` to check website display
4. (Optional) Add more records via backend

---

## Troubleshooting

### Menu not appearing in website
**Solution:** Check **Website → Menus** and ensure "Bimbingan Mahasiswa" menu is:
- ✅ Enabled (is_visible = True)
- ✅ Linked to correct URL (/bimbingan-mahasiswa)
- ✅ Parent menu set properly

### Records not showing on website
**Solution:**
- Make sure records have `is_published = True`
- Check `status` field (should not be archived)
- Verify demo data loaded: Check backend Daftar Bimbingan for 5 records

### 404 Error on /bimbingan-mahasiswa
**Solution:**
- Module needs upgrade/reinstall
- Check controller file exists: `controllers/main.py`
- Check templates file has correct ID: `id="bimbingan_index"`

### SEO Fields not auto-generating
**Solution:**
- Create/Save record → triggers @api.model.create() override
- Manual meta tags: Edit "SEO & Publikasi" tab
- Slug auto-computed on name change

---

## Future Enhancements

Possible improvements:
- [ ] Export guidance records to PDF
- [ ] Email notifications for status updates
- [ ] Guidance history/timeline view
- [ ] Attachment support (documents, files)
- [ ] Student feedback/rating system
- [ ] Integration with email for correspondence tracking
- [ ] Bulk import guidance data via Excel
- [ ] Dashboard/KPI metrics

---

## Support & Contact

For issues or questions about this module, please contact:
- Module Author: Andi Eka Nugraha
- Module Version: 1.0.0
- Last Updated: 2025-11-05

