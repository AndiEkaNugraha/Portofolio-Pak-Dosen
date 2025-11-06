# ⚙️ CONFIGURATION & QUICK START GUIDE

## 🚀 Quick Start (5 Menit)

### Step 1: Install Module
```
1. Pergi ke Odoo → Apps
2. Search: "Profil Dosen"
3. Klik Install
4. Wait for installation to complete
```

### Step 2: Access Menu
```
Pergi ke: Profil Dosen (Main Menu)
```

### Step 3: Buat Kategori (Optional - Sudah Ada Default)
```
Profil Dosen → Kategori Profil → Create
```

### Step 4: Tambah Profil Dosen
```
Profil Dosen → Data Profil Dosen → Create
Isi nama, kategori, info kontak → Save
```

### Step 5: Lihat di Website
```
Browser: http://your-odoo.com/profil
```

---

## 🔧 Backend Configuration

### A. Kategori Profil Setup

**Navigate to**: Profil Dosen → Kategori Profil

Default kategori yang tersedia:
- Profil Dosen Akademik
- Profil Dosen Teknis

Tambah kategori baru sesuai kebutuhan:
```
Name: [Nama Kategori]
Subtitle: [Deskripsi Singkat]
Dosen Category: [Akademik/Teknis/Profesional/Umum]
Description: [Penjelasan Lengkap]
```

### B. User Permissions

**File**: `security/ir.model.access.csv`

Permissions default:
- **Regular User**: Read-only access
- **Manager/HR**: Full CRUD access

Untuk ubah, edit file CSV atau via Odoo interface:
```
Settings → Technical → Access Rights → ir.model.access
```

### C. Form Configuration

**Semua fields opsional kecuali**:
- `name` (Nama Dosen)
- `blog_id` (Kategori)
- Tab Education: jenjang & institusi wajib
- Tab Skills: nama keahlian wajib

**Rich Text Fields** (bisa HTML):
- biography
- expertise_fields
- research_interest
- experience.description
- experience.achievements
- award.description

---

## 📱 Website Configuration

### A. Menu Placement

Untuk menambahkan link di website menu:

**Option 1**: Via Odoo Website Builder
```
Go to: Website → Configuration → Website Menus
Add: /profil → "Profil Dosen"
```

**Option 2**: Direct URL
```
http://your-domain/profil
```

### B. Theme Integration

Module ini kompatibel dengan theme apa pun karena:
- ✅ Menggunakan standard Odoo bootstrap CSS
- ✅ Custom CSS dapat di-override
- ✅ Responsive design compatible

### C. SEO Settings

Setiap profil memiliki:
- Unique slug untuk URL
- Meta title untuk browser tab
- Meta description untuk search engine
- Keywords untuk SEO

**Set otomatis**, atau manual di tab "SEO"

---

## 📊 Data Structure

### Relationship Diagram
```
profil.blog (Category)
    │
    └─── profil.post (Main Profile)
            │
            ├─── profil.education (Pendidikan)
            ├─── profil.skill (Keahlian)
            ├─── profil.experience (Pekerjaan)
            └─── profil.award (Penghargaan)
```

### Required Fields untuk Publish
```
profil.post:
├── name ...................... (Required)
├── blog_id ................... (Required)
├── is_published .............. (Default: True)

Minimal data:
└── At least name & category
```

---

## 🔒 Security & Privacy

### Access Control

**Levels of Access**:

1. **Database Level**: `ir.model.access.csv`
   - Read, Write, Create, Delete permissions per role

2. **Record Level** (Optional): Record rules
   - Currently: Anyone can read published profiles

3. **Website Level**: 
   - All published profiles visible
   - Only registered users can download CV (can be customized)

### Enable Authentication for CV Download

**Modify** `controllers/main.py`:
```python
# Change from:
@http.route('/profil/<slug>/download-cv', auth="public", website=True)

# To:
@http.route('/profil/<slug>/download-cv', auth="user", website=True)
```

---

## 📧 Email Integration

### Optional: Send Email on Publish

**To enable**, add this method ke `profil_post.py`:

```python
def action_publish(self):
    """Publish dan send notification email"""
    self.write({'is_published': True})
    
    # Send email notification
    if self.email:
        subject = f"Profil {self.name} telah dipublikasikan"
        body = f"Profil dosen {self.name} sekarang tersedia di website"
        
        mail_values = {
            'subject': subject,
            'body_html': body,
            'email_to': self.email,
        }
        self.env['mail.mail'].create(mail_values)
    
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Sukses',
            'message': 'Profil dan email notifikasi telah dikirim',
            'sticky': False,
        }
    }
```

---

## 🎨 Customization Guide

### A. Ubah Warna & Styling

**File**: `static/src/css/profil_style.css`

**Main Colors**:
```css
Primary: #667eea (gradient)
Secondary: #f093fb
Accent: #3498db
Dark: #2c3e50
```

**Change example**:
```css
/* Ubah warna utama dari biru ke merah */
.btn-primary {
    background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
}

.profil-card:hover {
    box-shadow: 0 5px 20px rgba(255, 75, 87, 0.3);
}
```

### B. Ubah Template Layout

**File**: `templates/profil_templates.xml`

**Example**: Ubah grid dari 3 kolom ke 2 kolom:
```xml
<!-- From: -->
<div class="col-lg-4 col-md-6 col-sm-12 mb32">

<!-- To: -->
<div class="col-lg-6 col-md-6 col-sm-12 mb32">
```

### C. Tambah Form Field di Backend

**File**: `models/profil_post.py`

```python
# Tambah field baru
specialized_field = fields.Char('Bidang Spesialisasi', translate=True)

# Di views/profil_views.xml, tambah field di form:
<field name="specialized_field"/>
```

### D. Add New Tab di Form

**File**: `views/profil_views.xml`

```xml
<page string="Tab Baru" name="tab_baru">
    <field name="field_name" widget="html"/>
</page>
```

---

## 🐛 Troubleshooting

### Problem: Module tidak muncul di Apps

**Solution**:
1. Refresh page (Ctrl+R)
2. Go to Settings → Technical → Modules → Update Modules List
3. Search "Profil" again

### Problem: Form tidak bisa disave

**Solution**:
- Check browser console (F12) untuk error
- Pastikan semua required field terisi
- Check server logs di terminal Odoo

### Problem: Website URL tidak work

**Solution**:
```
1. Pastikan is_published = True
2. Check slug name (tidak ada spasi)
3. Akses via: /profil/slug-name
4. Atau: /profil untuk list
```

### Problem: CSS tidak diterapkan

**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Restart Odoo
3. Go to Settings → Technical → Assets → Rebuild Assets

### Problem: Photo tidak muncul

**Solution**:
- File size: max 25MB (default Odoo)
- Format: JPG, PNG, GIF
- Recommended: 500x500px atau lebih
- Centang checkbox untuk publish

---

## 📈 Performance Tips

### Database Optimization
```sql
-- Untuk search lebih cepat, add index di slug:
CREATE INDEX idx_profil_post_slug ON profil_post(slug);
```

### Website Performance
1. **Image Optimization**
   - Gunakan image compression
   - Recommended: < 200KB per image

2. **Pagination**
   - Default: 12 profiles per page
   - Edit di `controllers/main.py`: `posts_per_page = 12`

3. **Caching**
   - Website list halaman bisa di-cache
   - Reduce server load

---

## 🔄 Backup & Restore

### Backup Database
```sql
-- PostgreSQL
pg_dump -U odoo database_name > backup.sql

-- Restore
psql -U odoo database_name < backup.sql
```

### Export Profil Data
1. Go to: Data Profil Dosen list
2. Click: Select All
3. Action: Export
4. Format: CSV, Excel, atau JSON

### Import Profil Data
1. Go to: Data Profil Dosen list
2. Action: Import
3. Upload file
4. Map fields
5. Import

---

## 📊 Reports (Future Enhancement)

Dapat di-extend untuk:
- Profile statistics report
- Education summary report
- Skills matrix report
- Awards & recognition report

---

## 🌐 Multi-Language Support

Module mendukung translate untuk:
- name (Nama Dosen)
- biography
- expertise_fields
- research_interest

Untuk enable multi-language:
1. Go to: Settings → Translate → Load Translation
2. Select language
3. Translate fields

---

## 🔐 GDPR Compliance

Module considerations:
- Personal data fields: name, email, phone, office
- CV files: binary storage
- Photos: image field

Untuk delete data:
```
Go to: Profil Post → Delete record
Cascade delete: All related education/skills/etc
```

---

## 📞 Support & Documentation

**Available Resources**:
- `README.md` - Module overview
- `IMPLEMENTATION_GUIDE.md` - Detailed setup
- `TESTING_DATA.md` - Example data
- `COMPLETION_SUMMARY.md` - Feature summary
- This file - Configuration & troubleshooting

---

## ✅ Final Checklist Before Going Live

- [ ] Module installed
- [ ] Permissions configured
- [ ] At least 1 category created
- [ ] At least 1 profile created & published
- [ ] Website URL working (/profil)
- [ ] Search & filter tested
- [ ] Mobile view tested
- [ ] CSS styling applied correctly
- [ ] Download CV working
- [ ] Email notifications setup (if desired)
- [ ] Backup created
- [ ] Documentation reviewed

---

**Ready to deploy!** 🚀

Last Updated: November 4, 2025
Version: 1.0.0
