# Troubleshooting: Bimbingan Mahasiswa 404 Error

## Problem
Menu "Bimbingan Mahasiswa" appears in website navigation but clicking it shows 404 error.

## Root Cause
Module is installed but routes are not yet active. Need to:
1. Upgrade module in Odoo
2. Restart Odoo service

---

## Solution: Step-by-Step

### Option 1: Upgrade via Odoo Backend (Recommended)

1. **Go to Apps module**
   - URL: `http://localhost:8069/odoo/action-181` (or search for "Apps")

2. **Remove module filter**
   - Click "Clear" or remove any filters
   
3. **Search for "Bimbingan"**
   - Should see: "Portofolio Dosen - Informasi Bimbingan Mahasiswa"

4. **Click the module**

5. **Click "Upgrade" button**
   - Wait for progress bar to complete

6. **Refresh page (F5)**

---

### Option 2: Upgrade via Terminal

If you have access to terminal where Odoo is running:

```powershell
# Stop Odoo (Ctrl+C in terminal)

# Restart Odoo with module update
cd "d:\bebas lah terserah kamu\port-pak-mada\Portofolio-Pak-Dosen"
# Run upgrade command (replace database name if different):
# ./odoo-bin -d <database> -u bimbingan_mahasiswa --no-http
```

Then restart normally.

---

### Option 3: Force Module Reload

1. **Go to Settings → Technical → Modules (Menu)**

2. **Search "Bimbingan Mahasiswa"**

3. **Click module**

4. **Click button "Upgrade Module" / "Reinstall"**

5. **Wait for reload**

---

## After Upgrade

Once upgraded, the following should work:

✅ `http://localhost:8069/bimbingan-mahasiswa` → List page with demo data  
✅ Click on any record → Detail page  
✅ "Tambah Bimbingan Baru" button → Form page  

---

## Verification Checklist

After upgrading, verify:

- [ ] URL `/bimbingan-mahasiswa` shows list (not 404)
- [ ] 5 demo records appear in list
- [ ] Search & filter dropdowns work
- [ ] Click "Lihat Detail" → shows detail page
- [ ] "Tambah Bimbingan Baru" button opens form
- [ ] Form submission creates new record

---

## If Still Getting 404

1. **Check Controller is Loaded**
   - Go to: Settings → Technical → Routes
   - Search for: `/bimbingan-mahasiswa`
   - Should show 4 routes

2. **Check Module Status**
   - Go to: Apps → Search "Bimbingan"
   - Should show: "Installed" status (not "Uninstalled")

3. **Check Logs**
   - Look at Odoo logs for any Python errors
   - Common errors: template not found, model not found, import errors

4. **Restart Odoo Service**
   - Full restart (not just upgrade) sometimes needed
   - Stop service → Wait 5s → Start service

---

## Contact Support

If issue persists after these steps, check:
1. Odoo version compatibility (module is for Odoo 17+)
2. Module XML files for syntax errors
3. Database connectivity issues
4. Browser cache (try incognito mode)

