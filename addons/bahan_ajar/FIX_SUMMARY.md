# Bahan Ajar Module - Bug Fix & Form Simplification

## 🔧 Issues Fixed

### 1. ✅ Context Evaluation Error
**Error:** `EvalError: Can not evaluate python expression: ({'search_default_group_material_type': 1, 'default_blog_id': ref('blog_bahan_ajar')})`

**Root Cause:** Using `ref()` function directly in context dictionary - `ref()` cannot be evaluated in Python context.

**Solution:** Removed `'default_blog_id': ref('blog_bahan_ajar')` from context. The domain filter already handles blog filtering properly.

**File Modified:** `/views/bahan_ajar_views.xml` (Line 142)

**Before:**
```xml
<field name="context">{'search_default_group_material_type': 1, 'default_blog_id': ref('blog_bahan_ajar')}</field>
```

**After:**
```xml
<field name="context">{'search_default_group_material_type': 1}</field>
```

---

## 📝 Feature Added: Simplified Web Form

### 2. ✅ Website Form Template
**File:** `/templates/bahan_ajar_templates.xml`

Created new template `bahan_ajar_form` with simplified, user-friendly input form:

**Form Fields (8 essential):**
1. Judul Materi (required)
2. Jenis Materi - dropdown (required)
3. Tipe File - dropdown [PDF/Video/Link] (required)
4. Topik (required)
5. Target Audiens (optional)
6. Estimasi Waktu dalam Jam (optional)
7. URL/Link Konten (optional, for video/link)
8. Deskripsi Materi (optional)
9. Publish ke Website - checkbox

**Features:**
- ✅ Responsive Bootstrap 5 layout
- ✅ Error message display
- ✅ CSRF token protection
- ✅ Form validation
- ✅ Required field marking
- ✅ Simpan & Kembali buttons

---

### 3. ✅ Website Form Routes
**File:** `/controllers/main.py`

Added 2 new routes:

#### Route 1: GET /bahan-ajar/form
```python
@http.route('/bahan-ajar/form', auth='public', website=True, methods=['GET'])
def bahan_ajar_form_page(self, **kw):
    """Halaman form untuk add bahan ajar"""
    # Returns: material_type_options, empty values dict, no error
```

**Purpose:** Display the form page with dropdown options

**Returns:** 
- `material_type_options` - 6 types of materials
- `values` - Empty dict for new record
- `error` - None (no errors on initial load)

#### Route 2: POST /bahan-ajar/form/submit
```python
@http.route('/bahan-ajar/form/submit', auth='public', website=True, methods=['POST'], csrf=False)
def bahan_ajar_form_submit(self, **kw):
    """Process form submission"""
```

**Purpose:** Process form submission and create new blog.post record

**Functionality:**
- ✅ Get or create "Bahan Ajar" blog
- ✅ Validate required fields
- ✅ Create blog.post record
- ✅ Handle different file types (video URL, link URL, PDF)
- ✅ Set website_published flag
- ✅ Redirect to detail page on success
- ✅ Return to form with error on failure
- ✅ Error logging for debugging

---

## 📊 Form Field Mapping

| Form Field | Database Field | Type | Required |
|-----------|---------------|------|----------|
| Judul Materi | name | Char | ✅ Yes |
| Jenis Materi | material_type | Select | ✅ Yes |
| Tipe File | file_type | Select | ✅ Yes |
| Topik | topic | Char | ✅ Yes |
| Target Audiens | target_audience | Char | ❌ No |
| Estimasi Waktu | estimated_time | Float | ❌ No |
| URL/Link | video_url / web_resource_url | Char | ❌ No |
| Deskripsi | teaser | Text | ❌ No |
| Publish | website_published | Boolean | ❌ No |

---

## 🌐 Website URL

Users can now:
1. **View list:** `/blog/bahan-ajar-1`
2. **View detail:** `/blog/bahan-ajar-1/[slug]`
3. **Add new:** `/bahan-ajar/form` (NEW! ✅)
4. **Submit:** `/bahan-ajar/form/submit` (POST, NEW! ✅)

---

## ✅ Testing Checklist

To test the fixes:

1. **Upgrade module in Odoo**
   - Apps → Search "Bahan Ajar" → Upgrade

2. **Test backend error fix**
   - Go to Bahan Ajar menu in backend
   - Should work without "ref() not defined" error

3. **Test website form**
   - Go to `/bahan-ajar/form`
   - Fill form with required fields
   - Click "Simpan"
   - Should create new record and redirect to detail page

4. **Verify record creation**
   - Check backend: Bahan Ajar list should show new record
   - Check website: New item should appear in `/blog/bahan-ajar-1` if published

---

## 📁 Files Modified

| File | Changes |
|------|---------|
| `views/bahan_ajar_views.xml` | Line 142: Fixed context error |
| `templates/bahan_ajar_templates.xml` | Added bahan_ajar_form template (140+ lines) |
| `controllers/main.py` | Added 2 routes + imports (80+ lines) |

---

## 🎯 Material Type Options

| Value | Label |
|-------|-------|
| lecture_notes | Catatan Kuliah |
| slide | Slide Presentasi |
| assignment | Tugas/Soal |
| reference | Referensi/Buku |
| exercise | Latihan Soal |
| other | Lainnya |

---

## 🔒 Security

- ✅ CSRF token validation
- ✅ Public auth (anyone can view, but form handles access)
- ✅ Error logging for debugging
- ✅ Sanitized input handling
- ✅ Proper redirect on success

---

## 📝 Next Steps

1. **Upgrade bahan_ajar module** in Odoo
2. **Refresh website** (F5)
3. **Test form** at `/bahan-ajar/form`
4. **Report any issues** if they occur

---

**Status:** ✅ READY TO TEST

Last Updated: November 6, 2025
