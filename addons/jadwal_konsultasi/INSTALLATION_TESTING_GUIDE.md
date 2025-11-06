# JADWAL KONSULTASI - INSTALLATION & TESTING GUIDE

## 🎯 Quick Installation

### Step 1: Verify Module Location
```bash
# The module should be at:
d:\bebas lah terserah kamu\port-pak-mada\Portofolio-Pak-Dosen\addons\jadwal_konsultasi\

# Verify all files exist:
ls addons/jadwal_konsultasi/
# Should show: __init__.py, __manifest__.py, controllers/, models/, views/, templates/, data/, security/, static/, README.md, COMPLETION_SUMMARY.md
```

### Step 2: Restart Odoo
```bash
# If using Docker:
docker-compose restart odoo_app

# If local service:
sudo systemctl restart odoo
```

### Step 3: Install Module
1. Open Odoo dashboard
2. Go to **Settings** (gear icon)
3. Click **Apps** menu
4. Click **Update Apps List** button
5. Search for: `jadwal konsultasi`
6. Click the module
7. Click **Install** button

### Step 4: Verify Installation
Wait 10-15 seconds for module to install, then verify:

✅ **Backend Menu:**
- Left sidebar should show "Jadwal Konsultasi" menu
- Click it to see list of schedules (should show 3 demo records)

✅ **Website:**
- Open browser and go to: `http://localhost:8069/jadwal-konsultasi`
- Should show schedule list with 3 demo records
- Try filtering by jenis/hari/lokasi
- Click "Lihat Detail" to see detail page

---

## 🧪 Testing Checklist

### Admin Interface Testing

#### Menu & Views
- [ ] Main menu "Jadwal Konsultasi" visible
- [ ] Menu shows all 3 demo records
- [ ] Kanban view displays cards
- [ ] Can switch to List view
- [ ] Can switch to Form view
- [ ] Search and filter work

#### Create New Record
```
1. Click Create button
2. Fill in:
   - Name: "Test Jadwal - Senin"
   - Hari: Senin
   - Jam Mulai: 09:00
   - Jam Selesai: 10:00
   - Jenis Konsultasi: Akademik
   - Tipe Lokasi: Ruangan
   - Lokasi Ruangan: B-100
   - Kapasitas Maksimal: 5
3. Click Save
```
- [ ] Record created successfully
- [ ] Shows in Kanban/List view
- [ ] Slug auto-generated (should be "test-jadwal-senin")

#### Edit & Delete
```
1. Click on created record
2. Modify: Kapasitas Maksimal = 8
3. Click Save
```
- [ ] Changes saved
- [ ] List updated

```
1. Click Delete button
2. Confirm deletion
```
- [ ] Record deleted
- [ ] List refreshed

#### Publish to Website
```
1. Open any record
2. Toggle "Published" to ON
3. Save
```
- [ ] Status changes
- [ ] Record appears on website

### Website Testing

#### List Page (`/jadwal-konsultasi`)
- [ ] Page loads without errors
- [ ] Shows all published records as cards
- [ ] Each card shows: name, hari, jam, jenis, lokasi, kuota
- [ ] Status badge appears (Tersedia/Penuh/Tidak Aktif)
- [ ] Progress bar shows kuota visual
- [ ] "Lihat Detail" button works

#### Filtering
```
Test Filter Jenis:
1. Select "Akademik" in filter dropdown
2. Check only akademik records show
```
- [ ] Filter by jenis works
- [ ] Filter by hari works
- [ ] Filter by lokasi works
- [ ] Multiple filters combine

#### Detail Page
```
Click "Lihat Detail" on any record
```
- [ ] Page shows full schedule info
- [ ] Hari, jam, jenis displays correctly
- [ ] Lokasi shows properly:
  - If ruangan: shows room number
  - If online: shows clickable link
  - If hybrid: shows both
- [ ] Kuota progress bar visible
- [ ] Status indicator shows
- [ ] "Kembali ke Daftar" button works

#### Responsive Design
```
Mobile Test:
1. Open in browser DevTools (F12)
2. Toggle Device Toolbar (Ctrl+Shift+M)
3. Select Mobile device
```
- [ ] List cards stack vertically
- [ ] Filters remain usable
- [ ] Detail page readable
- [ ] Buttons clickable
- [ ] No horizontal scroll

### Data Validation Testing

#### Demo Data Verification
```
Record 1: Konsultasi Akademik - Senin Pagi
- Name: ✅ Visible
- Hari: Senin (0) ✅
- Jam: 10:00-12:00 ✅
- Jenis: Akademik ✅
- Lokasi: Ruangan B-304 ✅
- Kapasitas: 5 ✅
```

```
Record 2: Konsultasi Skripsi - Rabu Sore
- Name: ✅ Visible
- Hari: Rabu (2) ✅
- Jam: 14:00-16:00 ✅
- Jenis: Skripsi ✅
- Lokasi: Hybrid ✅
- Kapasitas: 3 ✅
```

```
Record 3: Konsultasi Penelitian Online - Jumat
- Name: ✅ Visible
- Hari: Jumat (4) ✅
- Jam: 13:00-14:30 ✅
- Jenis: Penelitian ✅
- Lokasi: Online ✅
- Kapasitas: 10 ✅
```

### Security & Permissions Testing

#### Access Control
```
1. Logout from admin
2. Create new user with "User" role
3. Login as new user
4. Try to access "Jadwal Konsultasi" menu
```
- [ ] User can READ schedules
- [ ] User CANNOT create/edit/delete (read-only)

```
1. Login as admin
2. Create new user with "Manager" role
3. Login as new user
```
- [ ] Manager can create/edit schedules
- [ ] Manager cannot delete (requires System role)

### CSS & Styling Testing

#### Visual Elements
- [ ] Cards have proper spacing and shadows
- [ ] Badges display with correct colors:
  - Akademik: Blue
  - Penelitian: Red
  - Skripsi: Orange
  - etc.
- [ ] Status badge colors:
  - Tersedia: Green
  - Penuh: Yellow
  - Tidak Aktif: Red
- [ ] Progress bar fills correctly
- [ ] Font sizes readable
- [ ] Colors contrast sufficient

#### Hover & Interaction
- [ ] Cards have hover effect (lift up)
- [ ] Links underline on hover
- [ ] Buttons change color on hover
- [ ] Buttons clickable

### API Testing (Advanced)

#### Availability Endpoint
```bash
curl "http://localhost:8069/jadwal-konsultasi/konsultasi-akademik-senin-pagi/availability"
```
Expected response:
```json
{
  "status": "success",
  "is_available": true,
  "kuota_tersedia": 5,
  "kapasitas_maksimal": 5,
  "is_active": true
}
```

#### List Endpoint with Filter
```bash
curl "http://localhost:8069/jadwal-konsultasi?jenis_konsultasi=akademik"
```
- [ ] Returns filtered results

---

## 🐛 Common Issues & Solutions

### Issue: Module not appearing in Apps list
**Solution:**
1. Go to Settings > Apps > Update Apps List (click button)
2. Wait 30 seconds
3. Search again for "jadwal konsultasi"

### Issue: Website routes return 404
**Solution:**
1. Check Controllers > __init__.py exists and imports main
2. Restart Odoo: `docker-compose restart odoo_app`
3. Check Odoo logs for import errors

### Issue: Styling not loading on website
**Solution:**
1. Settings > Clear Cache
2. Hard refresh browser: Ctrl+Shift+Delete
3. Check CSS file: `static/src/css/jadwal_konsultasi.css` exists

### Issue: Detail page slug not working
**Solution:**
1. Check slug field is populated (computed field)
2. Verify record is published: `website_published = True`
3. Verify record is active: `is_active = True`

### Issue: Can't see records in menu
**Solution:**
1. Check records have `website_published = True`
2. Check records have `is_active = True`
3. Try refreshing page or logging out/in

---

## 📊 Expected Test Results

### Success Criteria ✅

All of the following should work:

1. **Backend Administration**
   - [ ] Create new schedule record
   - [ ] Edit existing record
   - [ ] Delete record
   - [ ] View in Kanban/List/Form
   - [ ] Search and filter
   - [ ] Publish/unpublish to website

2. **Website Frontend**
   - [ ] List page loads at `/jadwal-konsultasi`
   - [ ] Shows all published schedules
   - [ ] Filtering by jenis/hari/lokasi
   - [ ] Detail page works with slug URL
   - [ ] Responsive on mobile

3. **Data & Display**
   - [ ] Demo data visible (3 records)
   - [ ] Fields display correctly
   - [ ] Computed fields work (slug, website_url, kuota)
   - [ ] Formatting correct (jam display, hari display)

4. **Security**
   - [ ] Access control enforced
   - [ ] Only published records visible
   - [ ] Only active records visible
   - [ ] User roles respected

---

## 📝 Test Report Template

```
Date: _____________
Tester: _____________
Odoo Version: 19.0
Module Version: 1.0.0

RESULTS:
========
Backend Admin:      ✅ ❌ (Notes: _______________)
Website Frontend:   ✅ ❌ (Notes: _______________)
Data Validation:    ✅ ❌ (Notes: _______________)
Security:          ✅ ❌ (Notes: _______________)
Styling:           ✅ ❌ (Notes: _______________)

Overall Status: ✅ PASS / ❌ FAIL

Issues Found:
1. _____________________________
2. _____________________________
3. _____________________________
```

---

## 🎉 Final Verification

Once all tests pass, module is **PRODUCTION READY**:

- ✅ Installation completed
- ✅ All views working
- ✅ Website displays correctly
- ✅ Filtering functional
- ✅ Security enforced
- ✅ Styling applied
- ✅ No errors in logs

**Status: READY FOR DEPLOYMENT**

---

## 📞 Troubleshooting Support

If issues occur during testing:

1. **Check Odoo Logs:**
   ```bash
   tail -f /var/log/odoo/odoo-server.log
   ```

2. **Check Module Status:**
   - Settings > Apps > Search "jadwal konsultasi"
   - Click module and check status

3. **Review Documentation:**
   - See README.md for detailed info
   - Check COMPLETION_SUMMARY.md for feature matrix

4. **Verify Files:**
   - All files exist in addons/jadwal_konsultasi/
   - No file corruptions
   - Correct permissions set

---

**Happy Testing! 🚀**

For any issues, refer to README.md or COMPLETION_SUMMARY.md files included in the module.
