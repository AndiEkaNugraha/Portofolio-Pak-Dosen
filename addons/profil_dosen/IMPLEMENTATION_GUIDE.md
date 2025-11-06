# PANDUAN IMPLEMENTASI - PROFIL DOSEN MODULE

## 📋 Ringkasan Implementasi

Module **Profil Dosen** telah berhasil dibuat untuk Odoo 19 dengan struktur lengkap yang mengikuti best practices dari module `hki_paten`. Module ini memungkinkan pengelolaan profil lengkap dosen dengan semua informasi yang dibutuhkan.

---

## 🏗️ Struktur Lengkap Module

```
profil_dosen/
├── __init__.py                 # Main initialization
├── __manifest__.py             # Module manifest (metadata)
├── README.md                   # Documentation
│
├── models/                     # Backend Data Models
│   ├── __init__.py            
│   ├── profil_blog.py          # Kategori profil (inherit blog.blog)
│   ├── profil_post.py          # Data profil dosen utama
│   ├── profil_education.py     # Riwayat pendidikan
│   ├── profil_skill.py         # Bidang keahlian & minat riset
│   ├── profil_experience.py    # Riwayat pekerjaan & jabatan
│   └── profil_award.py         # Penghargaan & pengakuan
│
├── controllers/                # Website Routes
│   ├── __init__.py
│   └── main.py                 # Frontend controller
│
├── views/                      # Backend Views & Menus
│   ├── profil_views.xml        # Model views (list, form)
│   └── profil_menus.xml        # Menu structure
│
├── templates/                  # Website Templates
│   └── profil_templates.xml    # Frontend HTML pages
│
├── security/                   # Access Control
│   └── ir.model.access.csv     # Role-based permissions
│
├── data/                       # Initial Data
│   └── profil_data.xml         # Demo/default categories
│
└── static/                     # Static Assets
    ├── src/
    │   └── css/
    │       └── profil_style.css # Custom styling
    └── description/
        └── index.html          # Module description
```

---

## 📊 Data Models

### 1. **Profil Blog** (`profil.blog`)
- **Inherit dari**: `blog.blog`
- **Gunakan untuk**: Kategorisasi profil dosen
- **Fields utama**:
  - `dosen_category`: Akademik, Teknis, Profesional, Umum
  - `post_count`: Jumlah profil otomatis

### 2. **Profil Post** (`profil.post`)
- **Model utama** untuk data dosen
- **Fitur SEO**: slug, meta_title, meta_description, meta_keywords
- **Relasi one2many** ke education, skill, experience, award
- **Auto-generate slug** dari nama dosen

**Fields Utama:**
```
name                    → Nama dosen
blog_id                 → Kategori
image                   → Foto profil
nip                     → Nomor Induk Pegawai
email, phone, office    → Kontak
biography               → Biografi (HTML)
expertise_fields        → Keahlian (HTML)
research_interest       → Minat riset (HTML)
cv_file                 → File CV (binary)
is_published            → Publish ke website
slug                    → URL slug (auto)
```

### 3. **Profil Education** (`profil.education`)
- Riwayat pendidikan multi-level (S1-S3)
- Fields: jenjang, institusi, bidang, tahun, IPK, tesis

### 4. **Profil Skill** (`profil.skill`)
- Bidang keahlian dengan tingkat profisiensi
- Fields: nama, type, level, years, is_primary, keywords

### 5. **Profil Experience** (`profil.experience`)
- Timeline pekerjaan dan jabatan
- Fields: posisi, organisasi, periode, is_current, pencapaian

### 6. **Profil Award** (`profil.award`)
- Penghargaan & pengakuan
- Fields: nama, pemberi, tipe (intl/nasional), tingkat, sertifikat

---

## 🌐 Website Routes/URLs

| Route | Deskripsi | Template |
|-------|-----------|----------|
| `/profil` | Daftar semua profil | `profil_index` |
| `/profil/page/<n>` | Halaman dengan paginasi | `profil_index` |
| `/profil/<slug>` | Detail profil individu | `profil_detail` |
| `/profil/<slug>/download-cv` | Download CV | Controller |

---

## ✨ Fitur Utama

### Backend Features
✅ Interface form yang terstruktur dengan tabs
✅ Publish/Unpublish buttons
✅ Auto-generate slug dari nama
✅ SEO fields (meta title, description, keywords)
✅ Audit fields (create_date, write_date, users)
✅ Access control berbasis role

### Frontend Features
✅ Halaman daftar dengan search & filter
✅ Grid card responsif dengan foto
✅ Halaman detail dengan timeline
✅ Statistics dashboard
✅ Pagination
✅ Download CV functionality
✅ Modern styling dengan gradients
✅ Fully responsive (desktop, tablet, mobile)

---

## 🔒 Security & Access Control

File: `security/ir.model.access.csv`

```
Model                   | User Role        | Permissions
profil.blog            | user             | read
profil.blog            | erp_manager      | read, write, create, delete
profil.post            | user             | read
profil.post            | erp_manager      | read, write, create, delete
profil.education       | user             | read
profil.education       | erp_manager      | read, write, create, delete
profil.skill           | user             | read
profil.skill           | erp_manager      | read, write, create, delete
profil.experience      | user             | read
profil.experience      | erp_manager      | read, write, create, delete
profil.award           | user             | read
profil.award           | erp_manager      | read, write, create, delete
```

---

## 📝 SEO Configuration

Setiap profil memiliki:
1. **Slug**: URL-friendly identifier (auto-generated)
   - Contoh: `dr-ahmad-santoso` dari `Dr. Ahmad Santoso`

2. **Meta Title**: Untuk search engine (default: nama dosen)
   - Contoh: `Dr. Ahmad Santoso - Profil Dosen`

3. **Meta Description**: Preview di search results (auto dari teaser)
   - Contoh: `Biografi lengkap Dr. Ahmad Santoso dengan keahlian di bidang...`

4. **Meta Keywords**: Kata kunci yang relevan
   - Contoh: `dosen, profesor, teknologi, riset, Universitas`

---

## 🎨 Styling

File: `static/src/css/profil_style.css`

**Features:**
- Modern card-based design
- Timeline visualization untuk riwayat pendidikan & pekerjaan
- Gradient backgrounds
- Smooth hover effects
- Responsive breakpoints (768px, 992px, 1200px)
- Custom badges & buttons
- Clean typography

---

## 📦 Dependencies

Module ini memerlukan:
- `base` - Odoo base
- `website` - Website module
- `website_blog` - Blog module (untuk inherit)
- `mail` - Mail module

Kompatibel dengan **Odoo 19+**

---

## 🚀 Instalasi & Setup

### Step 1: Copy Module
```bash
cp -r profil_dosen /path/to/odoo/addons/
```

### Step 2: Install Module
1. Buka Odoo
2. Pergi ke **Apps** menu
3. Search "Profil Dosen"
4. Klik **Install**

### Step 3: Create Categories
1. Pergi ke **Profil Dosen** → **Kategori Profil**
2. Klik **Create**
3. Isi nama kategori (contoh: "Dosen Teknik Informatika")
4. Save

### Step 4: Add Dosen Profile
1. Pergi ke **Profil Dosen** → **Data Profil Dosen**
2. Klik **Create**
3. Isi form dengan detail dosen:
   - Nama dosen
   - Foto profil
   - NIP, Email, Telepon
   - Biografi lengkap
   - SEO fields

### Step 5: Add Related Data
- Klik tab **Pendidikan** → Tambah riwayat pendidikan
- Klik tab **Keahlian** → Tambah bidang keahlian
- Klik tab **Pekerjaan** → Tambah riwayat pekerjaan
- Klik tab **Penghargaan** → Tambah penghargaan

### Step 6: Upload CV & Publish
- Di tab **CV** → Upload file CV
- Centang **Tampilkan di Website**
- Save & Publish

### Step 7: View Website
- Buka browser ke `http://your-odoo.com/profil`
- Atau `http://your-odoo.com/profil/<slug>` untuk detail

---

## 💡 Tips Penggunaan

### Generate Slug Otomatis
Ketika membuat profil baru, slug akan otomatis di-generate dari nama dosen:
- "Dr. Ahmad Santoso" → `dr-ahmad-santoso`
- Bisa diedit manual jika diperlukan

### SEO Best Practices
1. Isi **Meta Title** dengan judul yang menarik & keyword-rich
2. Isi **Meta Description** dengan ringkasan 160 karakter
3. Tambahkan **Meta Keywords** yang relevan dengan bidang keahlian
4. Gunakan **slug yang deskriptif**

### Publikasi Bertahap
- Buat draft profil tanpa "Tampilkan di Website"
- Edit semua detail terlebih dahulu
- Baru publish saat siap

### Timeline Visibility
- **Riwayat Pendidikan**: Otomatis terurut dari tahun terbaru
- **Riwayat Pekerjaan**: Posisi "Saat Ini" ditandai dengan badge hijau
- **Penghargaan**: Bisa di-highlight dengan checkbox "Tampilkan di Highlight"

---

## 🔧 Customization

### Tambah Field Baru
Edit file model yang sesuai di `models/`:
```python
# Contoh: Tambah field di profil_post.py
new_field = fields.Char('Nama Field', help='Deskripsi')
```

### Ubah Styling
Edit `static/src/css/profil_style.css`:
```css
/* Custom styling */
.profil-card {
    /* Ubah styling di sini */
}
```

### Modify Template
Edit `templates/profil_templates.xml` untuk mengubah HTML/layout website

### Add Form Fields di Backend
Edit `views/profil_views.xml` untuk menambah field di form backend

---

## 📋 Checklist Implementasi

- ✅ 6 Models telah dibuat (Blog, Post, Education, Skill, Experience, Award)
- ✅ Controller dengan 3 routes (index, detail, download-cv)
- ✅ Backend views (list & form) dengan tabs
- ✅ Website templates (list & detail pages)
- ✅ Menu structure dengan action buttons
- ✅ Security access control
- ✅ Initial data (kategori default)
- ✅ CSS styling responsif
- ✅ SEO fields & slug auto-generate
- ✅ Publish/Unpublish functionality
- ✅ Search & filter functionality
- ✅ Pagination support
- ✅ Timeline visualization
- ✅ Download CV feature

---

## 🆘 Troubleshooting

### Module tidak muncul di Apps
- Refresh/restart Odoo
- Update modules list: Settings → Technical → Modules

### Slug tidak otomatis di-generate
- Pastikan nama dosen sudah diisi saat create
- Manual generate: edit form, kosongkan slug, save

### URL tidak ditemukan (404)
- Pastikan profil status "Tampilkan di Website" (is_published=True)
- Check slug name di URL

### CSS tidak diterapkan
- Clear browser cache
- Restart Odoo
- Check asset include di __manifest__.py

---

## 📞 Support

Untuk pertanyaan atau bug report:
- Buka issue di repository
- Contact author: Andi Eka Nugraha

---

**Last Updated**: November 4, 2025
**Version**: 1.0.0
**Odoo Version**: 19
