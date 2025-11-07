# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class MataKuliahPost(models.Model):
    _name = 'mata_kuliah.post'
    _inherit = 'blog.post'
    _description = 'Entri Mata Kuliah'

    # Override fields dari blog post
    name = fields.Char('Nama Mata Kuliah', required=True, translate=True)
    subtitle = fields.Char(string='Deskripsi Singkat', translate=True, help="Deskripsi singkat mata kuliah")
    blog_id = fields.Many2one('mata_kuliah.blog', 'Kategori Mata Kuliah', required=True, ondelete='cascade')

    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL slug yang SEO-friendly. Kosongkan untuk generate otomatis dari nama mata kuliah.")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan nama mata kuliah jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan deskripsi singkat jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")

    # Override blog fields dengan label yang jelas untuk mata kuliah
    teaser = fields.Char('Ringkasan', help="Ringkasan singkat mata kuliah")
    content = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap mata kuliah, silabus, atau informasi lainnya")

    # Hide/override problematic blog fields dari parent blog.post
    cover_properties = fields.Text(string="Cover Properties", default='{}', readonly=True)
    teaser_manual = fields.Html(string="Teaser Manual", readonly=True)

    # Explicitly override other blog fields that might cause confusion
    website_meta_title = fields.Char(string="Meta Title", readonly=True)
    website_meta_description = fields.Text(string="Meta Description", readonly=True)
    website_meta_keywords = fields.Char(string="Meta Keywords", readonly=True)

    # Field khusus mata kuliah
    course_code = fields.Char('Kode Mata Kuliah', required=True, help="Kode unik mata kuliah (contoh: IF101, MKU001)")
    semester = fields.Selection([
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
        ('3', 'Semester 3'),
        ('4', 'Semester 4'),
        ('5', 'Semester 5'),
        ('6', 'Semester 6'),
        ('7', 'Semester 7'),
        ('8', 'Semester 8'),
        ('odd', 'Ganjil'),
        ('even', 'Genap'),
        ('both', 'Ganjil & Genap'),
    ], string='Semester', required=True)

    academic_year_ids = fields.Many2many('academic.year', 'course_academic_year_rel', 'course_id', 'academic_year_id', string='Tahun Akademik', help="Tahun akademik pengajaran mata kuliah")
    sks = fields.Integer('SKS', required=True, help="Satuan Kredit Semester")
    course_type = fields.Selection([
        ('mandatory', 'Wajib'),
        ('elective', 'Pilihan'),
        ('specialization', 'Keahlian'),
    ], string='Tipe Mata Kuliah', default='mandatory')

    # Course details
    prerequisites = fields.Text('Prasyarat', help="Mata kuliah prasyarat yang harus ditempuh")
    learning_objectives = fields.Html('Capaian Pembelajaran', help="Capaian pembelajaran mata kuliah")
    syllabus_summary = fields.Html('Ringkasan Silabus', help="Ringkasan isi silabus mata kuliah")

    # Assessment methods
    assessment_methods = fields.Text('Metode Penilaian', help="Metode penilaian yang digunakan")

    # Student count
    max_students = fields.Integer('Kapasitas Maksimal', help="Jumlah mahasiswa maksimal per kelas")
    typical_students = fields.Integer('Jumlah Mahasiswa Rata-rata', help="Jumlah mahasiswa rata-rata per kelas")

    # Course materials/resources - now using related models
    textbook_ids = fields.One2many('course.textbook', 'course_id', string='Buku Referensi')
    resource_ids = fields.One2many('course.resource', 'course_id', string='Sumber Belajar Tambahan')

    # Keep old fields for backward compatibility (computed from new fields)
    textbooks = fields.Text('Buku Referensi (Legacy)', compute='_compute_legacy_fields', store=True)
    additional_resources = fields.Text('Sumber Belajar Tambahan (Legacy)', compute='_compute_legacy_fields', store=True)

    # Course evaluation
    student_satisfaction = fields.Float('Tingkat Kepuasan Mahasiswa', digits=(3, 2), help="Rata-rata tingkat kepuasan mahasiswa (skala 1-5)")
    course_rating = fields.Float('Rating Mata Kuliah', digits=(3, 2), help="Rating keseluruhan mata kuliah (skala 1-5)")

    def _generate_slug_from_name(self, name):
        """Generate SEO-friendly slug from name"""
        if not name:
            return ''
        import re
        # Convert to lowercase and replace special characters
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip('-')
        return slug

    @api.model
    def create(self, vals_list):
        """Auto-generate slug if not provided"""
        # Handle both single dict and list of dicts
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug_from_name(vals['name'])
                # Ensure uniqueness
                vals['slug'] = self._ensure_unique_slug(vals['slug'])

        return super(MataKuliahPost, self).create(vals_list)

    def write(self, vals):
        """Auto-regenerate slug if name changed and slug is empty"""
        if 'name' in vals and not vals.get('slug'):
            for record in self:
                if not record.slug:  # Only if slug is currently empty
                    vals['slug'] = self._generate_slug_from_name(vals.get('name', record.name))
                    vals['slug'] = record._ensure_unique_slug(vals['slug'], exclude_id=record.id)
        return super(MataKuliahPost, self).write(vals)

    def _ensure_unique_slug(self, slug, exclude_id=None):
        """Ensure slug is unique by adding number suffix if needed"""
        if not slug:
            return slug

        domain = [('slug', '=', slug)]
        if exclude_id:
            domain.append(('id', '!=', exclude_id))

        if self.search_count(domain) == 0:
            return slug

        # Add number suffix to make it unique
        counter = 1
        original_slug = slug
        while self.search_count([('slug', '=', slug)] + ([('id', '!=', exclude_id)] if exclude_id else [])) > 0:
            slug = f"{original_slug}-{counter}"
            counter += 1
        return slug

    @api.depends('textbook_ids', 'resource_ids')
    def _compute_legacy_fields(self):
        """Compute legacy text fields from new related models for backward compatibility"""
        for record in self:
            # Build textbooks text from related records
            if record.textbook_ids:
                textbooks_list = []
                for book in record.textbook_ids:
                    book_info = book.name
                    if book.author:
                        book_info += f" - {book.author}"
                    if book.publisher and book.year:
                        book_info += f" ({book.publisher}, {book.year})"
                    elif book.publisher:
                        book_info += f" ({book.publisher})"
                    elif book.year:
                        book_info += f" ({book.year})"
                    textbooks_list.append(book_info)
                record.textbooks = '\n'.join(textbooks_list)
            else:
                record.textbooks = ''

            # Build resources text from related records
            if record.resource_ids:
                resources_list = []
                for resource in record.resource_ids:
                    resource_info = resource.name
                    if resource.resource_type:
                        type_labels = {
                            'website': 'Website',
                            'video': 'Video',
                            'document': 'Dokumen',
                            'software': 'Software',
                            'other': 'Lainnya'
                        }
                        resource_info += f" ({type_labels.get(resource.resource_type, resource.resource_type)})"
                    if resource.url:
                        resource_info += f": {resource.url}"
                    if resource.description:
                        resource_info += f" - {resource.description}"
                    resources_list.append(resource_info)
                record.additional_resources = '\n'.join(resources_list)
            else:
                record.additional_resources = ''

    # Override website URL untuk halaman khusus dengan SEO-friendly URL
    def _compute_website_url(self):
        super(MataKuliahPost, self)._compute_website_url()
        for post in self:
            if post.id and post.blog_id and post.slug:
                post.website_url = f"/mata-kuliah/kuliah/{post.slug}-{post.id}"
            elif post.id and post.blog_id:
                post.website_url = f"/mata-kuliah/kuliah/{post.id}"

    def get_meta_title(self):
        """Get meta title for SEO"""
        return self.meta_title or self.name

    def get_meta_description(self):
        """Get meta description for SEO"""
        return self.meta_description or self.teaser or f"Mata kuliah: {self.name}"

    def get_meta_keywords(self):
        """Get meta keywords for SEO"""
        if self.meta_keywords:
            return self.meta_keywords
        keywords = []
        if self.course_code:
            keywords.append(self.course_code)
        if self.name:
            keywords.extend(self.name.split()[:3])  # First 3 words of course name
        return ', '.join(keywords) if keywords else ''

    @api.constrains('slug')
    def _check_slug_format(self):
        """Validate slug format"""
        for record in self:
            if record.slug:
                import re
                if not re.match(r'^[a-z0-9-]+$', record.slug):
                    raise ValueError("Slug hanya boleh mengandung huruf kecil, angka, dan tanda hubung (-)")
                if record.slug.startswith('-') or record.slug.endswith('-'):
                    raise ValueError("Slug tidak boleh diawali atau diakhiri dengan tanda hubung (-)")
                if '--' in record.slug:
                    raise ValueError("Slug tidak boleh mengandung tanda hubung ganda (--)")

    @api.onchange('name')
    def _onchange_name_generate_slug(self):
        """Auto-generate slug when name changes if slug is empty"""
        if self.name and not self.slug:
            self.slug = self._generate_slug_from_name(self.name)