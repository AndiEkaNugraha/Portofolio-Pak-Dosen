# Jadwal Konsultasi Module

## Overview
Modul **Jadwal Konsultasi** adalah sistem manajemen jadwal dan jam konsultasi dosen untuk mahasiswa dalam platform Odoo 19. Modul ini menyediakan backend management dan tampilan website interaktif untuk memudahkan mahasiswa mencari dan membooking slot konsultasi.

## Features

### Backend Management
- ✅ **Manajemen Jadwal**: Buat, edit, dan hapus jadwal konsultasi
- ✅ **Jadwal Berulang**: Atur hari dan jam konsultasi (Senin-Sabtu, jam custom)
- ✅ **Lokasi Fleksibel**: Dukung lokasi ruangan, online, atau hybrid
- ✅ **Jenis Konsultasi**: Kategorisasi konsultasi (akademik, penelitian, skripsi, karir, mentor, umum)
- ✅ **Manajemen Kapasitas**: Atur kapasitas maksimal per slot
- ✅ **SEO Friendly**: Automatic slug generation dan clean URLs
- ✅ **Publikasi**: Kontrol publikasi jadwal ke website

### Website Display
- ✅ **Jadwal List**: Tampilkan semua jadwal aktif dengan filtering
- ✅ **Detail Page**: Informasi lengkap per jadwal konsultasi
- ✅ **Responsive Design**: Mobile-friendly interface
- ✅ **Status Indicator**: Visual status (Tersedia, Kuota Penuh, Tidak Aktif)
- ✅ **Progress Bar**: Visualisasi kuota yang tersedia
- ✅ **Filtering**: Filter berdasarkan jenis, hari, lokasi

### Security & Access Control
- ✅ **Role-based Access**: User, Manager, System level permissions
- ✅ **Website Public Access**: Jadwal published otomatis muncul di website
- ✅ **Tracking**: View count dan audit trail

## Module Structure

```
jadwal_konsultasi/
├── __init__.py                           # Package initialization
├── __manifest__.py                       # Module manifest (dependencies, data files)
├── controllers/
│   ├── __init__.py                      # Controllers package
│   └── main.py                          # HTTP routes (list, detail, AJAX endpoints)
├── models/
│   ├── __init__.py                      # Models package
│   └── jadwal_konsultasi.py             # Main model (20+ fields)
├── views/
│   ├── jadwal_konsultasi_views.xml      # Backend views (Kanban, List, Form, Search)
│   ├── jadwal_konsultasi_menus.xml      # Admin menu hierarchy
│   └── assets.xml                       # Frontend assets
├── templates/
│   └── jadwal_konsultasi_templates.xml  # Qweb templates for website
├── data/
│   ├── jadwal_konsultasi_data.xml       # Static data
│   ├── jadwal_konsultasi_demo.xml       # Demo records
│   └── website_data.xml                 # Website menu integration
├── security/
│   └── ir.model.access.csv              # Access control rules
├── static/
│   └── src/
│       └── css/
│           └── jadwal_konsultasi.css    # Frontend styling
└── README.md                            # This file
```

## Models

### jadwal.konsultasi
Model utama untuk menyimpan jadwal konsultasi dosen.

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Nama/judul jadwal konsultasi |
| description | Html | Deskripsi detail konsultasi |
| sequence | Integer | Urutan tampilan di list |
| is_active | Boolean | Status aktif/tidak aktif |
| website_published | Boolean | Status publikasi ke website |
| view_count | Integer | Jumlah kali halaman diakses |
| **Schedule Fields** | | |
| hari_konsultasi | Selection | Hari dalam seminggu (0=Senin, 1=Selasa, ... 6=Minggu) |
| jam_mulai | Float | Jam mulai konsultasi (contoh: 10.5 = 10:30) |
| jam_selesai | Float | Jam selesai konsultasi |
| durasi_slot | Integer | Durasi setiap slot dalam menit |
| **Location Fields** | | |
| tipe_lokasi | Selection | Tipe lokasi (ruangan, online, hybrid) |
| lokasi_ruangan | Char | Nomor/nama ruangan |
| lokasi_online | Char | Link meeting online (Zoom, Google Meet, dll) |
| **Consultation Type** | | |
| jenis_konsultasi | Selection | Tipe konsultasi (akademik, penelitian, skripsi, karir, mentor, umum) |
| **Capacity** | | |
| kapasitas_maksimal | Integer | Jumlah mahasiswa max per slot |
| peserta_terdaftar | Integer | Jumlah yang sudah mendaftar |
| kuota_tersedia | Computed | Sisa kuota (kapasitas - peserta) |
| **Info** | | |
| syarat_konsultasi | Html | Syarat dan ketentuan |
| persiapan_mahasiswa | Html | Persiapan yang diperlukan mahasiswa |
| slug | Computed | URL-friendly name |
| website_url | Computed | Full website URL |
| tanggal_dibuat | Datetime | Tanggal pembuatan record |
| tanggal_diubah | Datetime | Tanggal perubahan terakhir |

#### Methods

- **get_hari_display()**: Mengembalikan nama hari dalam bahasa Indonesia
- **get_jam_mulai_display()**: Format jam mulai (HH:MM)
- **get_jam_selesai_display()**: Format jam selesai (HH:MM)
- **is_kuota_penuh()**: Check apakah kuota sudah penuh
- **is_available_now()**: Check apakah jadwal sedang berlangsung

## Routes

### Public Routes (No Authentication Required)

#### GET `/jadwal-konsultasi`
Tampilkan daftar semua jadwal konsultasi aktif dan published.

**Query Parameters:**
- `jenis_konsultasi`: Filter berdasarkan jenis (akademik, penelitian, dll)
- `hari_konsultasi`: Filter berdasarkan hari (0-6)
- `tipe_lokasi`: Filter berdasarkan tipe lokasi (ruangan, online, hybrid)

**Response:** Rendered HTML list dengan filter options

**Example:**
```
GET /jadwal-konsultasi?jenis_konsultasi=akademik&hari_konsultasi=0
```

#### GET `/jadwal-konsultasi/<slug>`
Tampilkan detail satu jadwal konsultasi berdasarkan slug.

**Response:** Rendered HTML detail page dengan informasi lengkap

**Example:**
```
GET /jadwal-konsultasi/konsultasi-akademik-senin-pagi
```

#### GET `/jadwal-konsultasi/<slug>/availability` (AJAX)
Check ketersediaan jadwal secara real-time (JSON API).

**Response:**
```json
{
  "status": "success",
  "is_available": true,
  "kuota_tersedia": 3,
  "kapasitas_maksimal": 5,
  "is_active": true
}
```

### Authenticated Routes (User Login Required)

#### POST `/jadwal-konsultasi/<slug>/book` (AJAX)
Melakukan booking/pendaftaran konsultasi (future feature).

**Request Body:**
```json
{
  "slug": "konsultasi-akademik-senin-pagi"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Berhasil mendaftar konsultasi",
  "kuota_tersedia": 2
}
```

## Views

### Backend (Admin Interface)

1. **Kanban View** (Default)
   - Card layout dengan nama, hari, jam, jenis
   - Quick action buttons
   - Drag-drop untuk reorder

2. **List View**
   - Tree layout dengan kolom: name, hari, jam_mulai, jam_selesai, jenis, tipe_lokasi, kapasitas
   - Sortable columns
   - Bulk actions

3. **Form View** (6 Tabs)
   - **Dasar**: Nama, sequence, status aktif/publish
   - **Jadwal**: Hari, jam, durasi slot
   - **Lokasi**: Tipe lokasi dengan field ruangan/online
   - **Kapasitas**: Kapasitas maksimal, peserta, kuota
   - **Syarat**: Syarat & persiapan mahasiswa
   - **Metadata**: Tanggal dibuat/diubah, view count

4. **Search View**
   - Filters: Aktif, Tidak Aktif, Kuota Penuh, Published
   - Group by: Hari, Jenis Konsultasi, Tipe Lokasi

### Frontend (Website)

1. **List Page** (`/jadwal-konsultasi`)
   - Card grid layout
   - Filter bar (jenis, hari, lokasi)
   - Status indicator (Tersedia, Kuota Penuh, Tidak Aktif)
   - Progress bar untuk kuota
   - Link ke detail page

2. **Detail Page** (`/jadwal-konsultasi/<slug>`)
   - Informasi lengkap jadwal
   - Sidebar dengan info booking
   - Progress bar kuota
   - Syarat & persiapan section
   - Back to list button

## Installation

### Prerequisites
- Odoo 19.0
- Database setup dengan modules: base, website, mail, calendar

### Steps

1. **Kopilkan module ke addons directory:**
```bash
cp -r jadwal_konsultasi /path/to/odoo/addons/
```

2. **Update module list di Odoo:**
   - Buka Settings > Apps > Update Apps List

3. **Install module:**
   - Search "Jadwal Konsultasi"
   - Click Install

4. **Verify installation:**
   - Check backend menu: Jadwal Konsultasi
   - Check website: `/jadwal-konsultasi`

## Usage

### Create Jadwal Konsultasi

1. Go to Menu: **Jadwal Konsultasi**
2. Click **Create** button
3. Fill in:
   - **Name**: Judul jadwal (contoh: "Konsultasi Akademik - Senin Pagi")
   - **Hari**: Pilih hari
   - **Jam Mulai/Selesai**: Atur jam
   - **Jenis**: Pilih tipe konsultasi
   - **Lokasi**: Pilih tipe dan isi lokasi detail
   - **Kapasitas**: Atur jumlah slot max
4. Click **Save**
5. Toggle **Published** untuk muncul di website

### Edit/Delete
- Click jadwal dari list
- Edit fields yang diperlukan
- Click **Save** atau **Delete**

### Website Display
- Auto muncul di `/jadwal-konsultasi` setelah publish
- Dapat di-filter oleh mahasiswa
- Link ke detail page otomatis dari slug

## Demo Data

Module includes 3 sample records:

1. **Konsultasi Akademik - Senin Pagi**
   - Senin 10:00-12:00
   - Lokasi: Ruangan B-304
   - Kapasitas: 5 peserta

2. **Konsultasi Skripsi - Rabu Sore**
   - Rabu 14:00-16:00
   - Lokasi: Hybrid (Ruangan B-305 + Zoom)
   - Kapasitas: 3 peserta

3. **Konsultasi Penelitian Online - Jumat**
   - Jumat 13:00-14:30
   - Lokasi: Google Meet
   - Kapasitas: 10 peserta

Demo data dapat dihapus setelah melakukan testing.

## Styling

Module includes comprehensive CSS dengan:
- Responsive card layout
- Color-coded status badges
- Progress bar untuk kuota
- Mobile-friendly design
- Print-friendly styles

### CSS Classes (untuk customization)
- `.o_jadwal_konsultasi_card` - Card container
- `.o_jadwal_status` - Status badge
- `.o_jadwal_kuota-bar` - Capacity progress bar
- `.badge-jenis` - Consultation type badge
- `.o_jadwal_lokasi` - Location display

## Security

### Access Control Levels

| Role | Permissions |
|------|-------------|
| **User** | Read-only |
| **Manager** | Create, Read, Update |
| **System** | Full access (Create, Read, Update, Delete) |

### Website Security
- Hanya jadwal dengan `website_published=True` yang tampil
- Hanya jadwal `is_active=True` yang tampil
- View count increment automatic
- No unauthorized access to unpublished content

## Future Enhancements

### Planned Features
- [ ] Email notification untuk booking confirmation
- [ ] Calendar view integration
- [ ] Mahasiswa booking form dengan validasi
- [ ] SMS reminder untuk jadwal konsultasi
- [ ] Rating & review system
- [ ] Attendance tracking
- [ ] Automatic reschedule notification
- [ ] Synchronize dengan Outlook/Google Calendar

### API Extensions
- [ ] REST API untuk mobile apps
- [ ] GraphQL endpoint
- [ ] Export ke iCal format

## Troubleshooting

### Jadwal tidak muncul di website
1. Check: `is_active = True` ✓
2. Check: `website_published = True` ✓
3. Refresh: Clear browser cache
4. Verify: Module installed dan aktif

### Styling tidak muncul
1. Clear assets cache: Settings > Clear Cache
2. Hard refresh browser: Ctrl+Shift+Delete
3. Check CSS file path di assets.xml

### Routes 404 error
1. Verify: controllers/__init__.py exists
2. Check: main.py syntax correct
3. Restart: Odoo service

## Support & Documentation

- **Database**: Odoo 19.0 PostgreSQL
- **API Documentation**: See routes section above
- **Code Standards**: Python PEP8, Odoo best practices
- **License**: LGPL-3

## Author
Andi Eka Nugraha

## Version
1.0.0 - Initial Release
