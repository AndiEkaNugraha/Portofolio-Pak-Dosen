# Petunjuk Menambah Bahan Ajar Baru

## 📋 Cara 1: Melalui Interface Web Odoo (Recommended)

### Langkah-langkah:

1. **Login ke Odoo**
   - Buka browser: `http://localhost:8069`
   - Login dengan akun admin

2. **Navigasi ke Menu Bahan Ajar**
   - Di website: Klik menu **Bahan Ajar** di header
   - Atau di Odoo: Pergi ke **Bahan Ajar** → **Bahan Ajar**

3. **Buat Bahan Ajar Baru**
   - Klik tombol **Create** (atau **+ Bahan Ajar**)
   - Isi form dengan data berikut:

### Form Input:

**Informasi Dasar:**
- **Title (Judul Materi)**: Nama materi pembelajaran
- **Author**: Otomatis terisi (admin)
- **Blog**: Pilih "Bahan Ajar"

**Tipe Konten:**
- **Content Type (file_type)**: 
  - `PDF Document` - Untuk file PDF
  - `Video Content` - Untuk video
  - `Web Resource` - Untuk link eksternal

**Deskripsi Materi:**
- **Description**: Penjelasan lengkap tentang materi (bisa gunakan HTML)
- **Learning Objectives**: Tujuan pembelajaran

**Metadata:**
- **Topic/Subject Area**: Topik utama materi
- **Material Type**: 
  - `Lecture Notes` - Materi kuliah
  - `Assignment/Exercise` - Tugas/latihan
  - `Reference Material` - Referensi
  - `Supplementary Material` - Materi tambahan
- **Target Level**:
  - `Basic Level` - Pemula
  - `Intermediate Level` - Menengah
  - `Advanced Level` - Lanjut
- **Estimated Study Time**: Waktu belajar estimasi (dalam jam)

**Konten Berdasarkan Tipe:**

Jika tipe **PDF**:
- Upload file PDF di field **PDF File**

Jika tipe **Video**:
- Paste URL video di field **Video URL** (contoh: YouTube, Vimeo)

Jika tipe **Web Resource**:
- Paste URL di field **Resource URL**

**Publikasi:**
- **Published**: Centang untuk mempublikasikan
- **Downloadable**: Centang jika ingin file bisa diunduh

4. **Simpan dan Publikasikan**
   - Klik **Save**
   - Klik **Publish** (jika ingin langsung visible di website)

---

## 📝 Cara 2: Melalui XML Data File

Untuk menambahkan data dalam jumlah besar atau sebagai demo data, edit file:

**Lokasi:** `addons/bahan_ajar/data/blog_data.xml`

### Template Standar:

```xml
<!-- Blog Post Baru: [Nama Materi] -->
<record id="blog_post_[slug_name]" model="blog.post">
    <field name="name">Judul Materi Pembelajaran</field>
    <field name="blog_id" ref="blog_bahan_ajar"/>
    <field name="author_id" ref="base.user_admin"/>
    <field name="content"><![CDATA[
        <h2>Judul Materi</h2>
        <p>Deskripsi singkat materi...</p>
        
        <h3>Topik yang Dibahas:</h3>
        <ul>
            <li>Topik 1</li>
            <li>Topik 2</li>
            <li>Topik 3</li>
        </ul>
        
        <p>Penjelasan lebih lanjut...</p>
    ]]></field>
    <field name="file_type">pdf</field>
    <field name="material_type">lecture</field>
    <field name="topic">Topik Utama</field>
    <field name="target_audience">basic</field>
    <field name="website_published" eval="True"/>
    <field name="is_published" eval="True"/>
    <field name="post_date" eval="datetime.now()"/>
</record>
```

### Contoh Penambahan PDF:

```xml
<!-- Blog Post: Algoritma Dasar -->
<record id="blog_post_algoritma" model="blog.post">
    <field name="name">Algoritma Dasar - Sorting &amp; Searching</field>
    <field name="blog_id" ref="blog_bahan_ajar"/>
    <field name="author_id" ref="base.user_admin"/>
    <field name="content"><![CDATA[
        <h2>Algoritma Dasar: Sorting &amp; Searching</h2>
        <p>Materi pembelajaran tentang algoritma fundamental dalam programming.</p>
        
        <h3>Topik:</h3>
        <ul>
            <li>Bubble Sort</li>
            <li>Merge Sort</li>
            <li>Quick Sort</li>
            <li>Binary Search</li>
            <li>Linear Search</li>
        </ul>
    ]]></field>
    <field name="file_type">pdf</field>
    <field name="material_type">lecture</field>
    <field name="topic">Algorithms</field>
    <field name="target_audience">basic</field>
    <field name="website_published" eval="True"/>
    <field name="is_published" eval="True"/>
    <field name="post_date" eval="datetime.now()"/>
</record>
```

### Contoh Penambahan Video:

```xml
<!-- Blog Post: React Hooks Tutorial -->
<record id="blog_post_react_hooks" model="blog.post">
    <field name="name">React Hooks Tutorial - useState &amp; useEffect</field>
    <field name="blog_id" ref="blog_bahan_ajar"/>
    <field name="author_id" ref="base.user_admin"/>
    <field name="content"><![CDATA[
        <h2>Mengenal React Hooks</h2>
        <p>Tutorial video tentang menggunakan React Hooks dalam modern React development.</p>
        
        <h3>Materi yang Dibahas:</h3>
        <ul>
            <li>Pengenalan Hooks</li>
            <li>useState Hook</li>
            <li>useEffect Hook</li>
            <li>Custom Hooks</li>
        </ul>
    ]]></field>
    <field name="file_type">video</field>
    <field name="video_url">https://www.youtube.com/watch?v=example-react</field>
    <field name="material_type">lecture</field>
    <field name="topic">Frontend Development</field>
    <field name="target_audience">intermediate</field>
    <field name="website_published" eval="True"/>
    <field name="is_published" eval="True"/>
    <field name="post_date" eval="datetime.now()"/>
</record>
```

### Contoh Penambahan Link Resource:

```xml
<!-- Blog Post: Web Design Resources -->
<record id="blog_post_web_design" model="blog.post">
    <field name="name">Koleksi Web Design Resources &amp; Tools</field>
    <field name="blog_id" ref="blog_bahan_ajar"/>
    <field name="author_id" ref="base.user_admin"/>
    <field name="content"><![CDATA[
        <h2>Web Design Resources</h2>
        <p>Kumpulan tool &amp; resource untuk web design yang berguna.</p>
        
        <h3>Kategori:</h3>
        <ul>
            <li>Design Tools (Figma, Adobe XD)</li>
            <li>Icon Library</li>
            <li>Font Resources</li>
            <li>Color Palette Tools</li>
        </ul>
    ]]></field>
    <field name="file_type">link</field>
    <field name="web_resource_url">https://example.com/web-design-resources</field>
    <field name="material_type">supplementary</field>
    <field name="topic">Web Design</field>
    <field name="target_audience">basic</field>
    <field name="website_published" eval="True"/>
    <field name="is_published" eval="True"/>
    <field name="post_date" eval="datetime.now()"/>
</record>
```

---

## ⚙️ Cara 3: Via Database (Advanced)

Jika Anda familiar dengan SQL, bisa langsung insert ke database:

```sql
INSERT INTO blog_post (
    name, content, blog_id, file_type, material_type, 
    topic, target_audience, website_published, is_published
) VALUES (
    'Judul Materi',
    'Konten HTML...',
    1,  -- ID blog bahan_ajar
    'pdf',  -- atau video, link
    'lecture',
    'Topik',
    'basic',
    true,
    true
);
```

---

## 📋 Daftar Field yang Tersedia:

| Field | Tipe | Required | Deskripsi |
|-------|------|----------|-----------|
| name | String | ✅ | Judul materi |
| content | HTML | ⚠️ | Deskripsi materi (bisa kosong) |
| file_type | Selection | ✅ | pdf, video, link |
| material_type | Selection | ✅ | lecture, assignment, reference, supplementary |
| topic | String | ✅ | Topik utama |
| target_audience | Selection | ✅ | basic, intermediate, advanced |
| pdf_file | Binary | ⚠️ | File PDF (jika file_type=pdf) |
| pdf_filename | String | ⚠️ | Nama file PDF |
| video_url | String | ⚠️ | URL video (jika file_type=video) |
| web_resource_url | String | ⚠️ | URL resource (jika file_type=link) |
| learning_objectives | Text | ❌ | Tujuan pembelajaran |
| estimated_time | Float | ❌ | Durasi dalam jam |
| website_published | Boolean | ❌ | Publish ke website |
| is_published | Boolean | ❌ | Status published |

**Legenda:**
- ✅ = Wajib diisi
- ⚠️ = Wajib tergantung tipe
- ❌ = Opsional

---

## 🔄 Upgrade Module Setelah Perubahan

Jika menambah data via XML:

1. Pergi ke **Modules** di Odoo
2. Cari module **bahan_ajar**
3. Klik **Upgrade** (atau tekan Ctrl+Shift+R untuk refresh)

---

## ✅ Checklist Sebelum Publish

- [ ] Judul materi sudah jelas dan deskriptif
- [ ] Tipe konten sesuai dengan materi
- [ ] Topik sudah dikategorikan dengan benar
- [ ] Target audience sesuai tingkat kesulitan
- [ ] Deskripsi sudah lengkap dan informatif
- [ ] File/URL sudah valid (jika ada)
- [ ] Materi sudah di-publish

---

## 🎯 Best Practices

1. **Penamaan Slug**: Gunakan lowercase dan dash
   - ❌ Blog Post Python Programming
   - ✅ blog_post_python_programming

2. **Konten HTML**: Gunakan CDATA untuk konten HTML yang kompleks
   ```xml
   <field name="content"><![CDATA[
       <h2>Judul</h2>
       <p>Paragraf...</p>
   ]]></field>
   ```

3. **Escape Karakter Khusus**: Gunakan &amp; untuk ampersand
   ```xml
   <field name="name">Django &amp; Flask</field>
   ```

4. **Urutan Materi**: Gunakan sequence untuk ordering
   ```xml
   <field name="sequence">10</field>
   ```

---

**Pertanyaan?** Hubungi administrator sistem atau lihat dokumentasi lebih lanjut.
