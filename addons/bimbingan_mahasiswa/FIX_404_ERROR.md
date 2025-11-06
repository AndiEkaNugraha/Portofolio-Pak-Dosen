# CARA FIX: Bimbingan Mahasiswa 404 Error

## ⚠️ MASALAH
Url `/bimbingan-mahasiswa` menunjukkan 404 error

## 🔧 SOLUSI CEPAT (5 menit)

### Langkah 1: Buka Apps Module
- URL: `http://localhost:8069/odoo/action-181`
- Atau: Click menu Odoo → Apps

### Langkah 2: Cari Module
- Di search box, ketik: **Bimbingan**
- Cari "Portofolio Dosen - Informasi Bimbingan Mahasiswa"

### Langkah 3: Upgrade
- Click module
- Click tombol **"Upgrade"** (warna biru)
- Tunggu sampai progress selesai

### Langkah 4: Refresh Website
- Kembali ke `http://localhost:8069/bimbingan-mahasiswa`
- Tekan F5 (refresh)
- Sekarang harus bisa! ✅

---

## Kalau Masih Tidak Mau Jalan

### Opsi A: Uninstall & Install Ulang
1. Apps → Search "Bimbingan"
2. Click module → Click "Uninstall"
3. Tunggu proses
4. Refresh page
5. Click "Install"
6. Tunggu selesai

### Opsi B: Restart Odoo Service
Jika ada akses terminal:
```powershell
# Restart layanan Odoo
```

---

## Setelah Berhasil, Cek:

✅ `/bimbingan-mahasiswa` → List halaman dengan 5 data demo  
✅ Klik nama record → Lihat detail  
✅ Klik "Tambah Bimbingan Baru" → Form buka  
✅ Isi form & submit → Record baru dibuat  

---

## Masih Tidak Jalan?

Cek di Backend:
1. Settings → Technical → Modules (Menu)
2. Cari "Bimbingan"
3. Lihat status: Apakah "Installed" atau "Uninstalled"?

Jika "Uninstalled" = Lakukan langkah Upgrade/Install lagi

---

## Detail Teknis (Untuk Admin)

Module ini memiliki:
- ✅ Model: `bimbingan.mahasiswa` (35+ fields)
- ✅ Controller: 4 routes (`/bimbingan-mahasiswa`, `/bimbingan-mahasiswa/<slug>`, form routes)
- ✅ Templates: 3 halaman (index, detail, form)
- ✅ Demo data: 5 records siap pakai
- ✅ Website menu: Auto-created di data.xml

Setelah upgrade, semua routes akan aktif dan accessible.
