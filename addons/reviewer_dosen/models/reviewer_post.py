# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ReviewerType(models.Model):
    _name = 'reviewer.type'
    _description = 'Jenis Aktivitas Review'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Jenis Review', required=True)
    code = fields.Char('Kode', required=True)
    description = fields.Text('Deskripsi')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)


class ReviewerPublisher(models.Model):
    _name = 'reviewer.publisher'
    _description = 'Penerbit/Institusi'
    _order = 'name'
    
    name = fields.Char('Nama Penerbit/Institusi', required=True)
    publisher_type = fields.Selection([
        ('journal', 'Penerbit Jurnal'),
        ('conference', 'Penyelenggara Konferensi'),
        ('publisher', 'Penerbit Buku'),
        ('university', 'Universitas'),
        ('research_institute', 'Lembaga Penelitian'),
        ('funding_agency', 'Lembaga Pendanaan'),
        ('other', 'Lainnya'),
    ], string='Jenis', required=True, default='journal')
    
    country = fields.Char('Negara')
    website_url = fields.Char('Website', help="URL website penerbit/institusi")
    email = fields.Char('Email')
    address = fields.Text('Alamat')
    description = fields.Text('Deskripsi')
    
    # Indexing info
    indexing_info = fields.Text('Informasi Indexing', help="Informasi tentang indexing (Scopus, WoS, dll)")
    
    active = fields.Boolean('Aktif', default=True)
    
    # Relations
    reviewer_post_ids = fields.One2many('reviewer.post', 'publisher_id', string='Aktivitas Review')


class ReviewerPost(models.Model):
    _name = 'reviewer.post'
    _description = 'Entri Aktivitas Review'
    _order = 'review_date desc, id desc'
    
    # Basic fields
    name = fields.Char('Judul Karya yang Direview', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul atau deskripsi singkat")
    blog_id = fields.Many2one('reviewer.blog', 'Kategori Review', required=True, ondelete='cascade')
    
    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL friendly untuk website, akan dibuat otomatis jika kosong")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan judul jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan ringkasan jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
    website_url = fields.Char('Website URL', compute='_compute_website_url', store=False, help="URL untuk halaman detail di website")
        
    # Content fields
    teaser = fields.Text('Ringkasan', help="Ringkasan singkat aktivitas review untuk preview dan website")
    content = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap aktivitas review", sanitize=False)
    
    # Cover photo
    cover_image = fields.Binary('Foto Cover', attachment=True, help="Foto cover untuk aktivitas review")
    cover_image_filename = fields.Char('Nama File Cover')
    
    # Publication fields 
    is_published = fields.Boolean('Tampilkan di Website', default=True, help="Centang untuk menampilkan aktivitas ini di website portofolio")
    active = fields.Boolean('Active', default=True)
    website_published = fields.Boolean('Published on Website', related='is_published', readonly=True)
    
    # Audit fields
    create_date = fields.Datetime('Created on', readonly=True)
    write_date = fields.Datetime('Last Updated on', readonly=True)
    create_uid = fields.Many2one('res.users', 'Created by', readonly=True)
    write_uid = fields.Many2one('res.users', 'Last Updated by', readonly=True)
    
    # Field khusus Aktivitas Review
    
    # Jenis aktivitas review
    reviewer_type_id = fields.Many2one('reviewer.type', 'Jenis Review', required=True)
    
    # Author/Researcher information
    author_name = fields.Char('Nama Penulis/Peneliti', required=True, 
                              help="Nama penulis atau peneliti yang karyanya direview")
    author_affiliation = fields.Char('Afiliasi Penulis', help="Institusi asal penulis")
    author_country = fields.Char('Negara Penulis')
    
    # Publisher/Organizer information
    publisher_id = fields.Many2one('reviewer.publisher', 'Penerbit/Institusi')
    journal_conference_name = fields.Char('Nama Jurnal/Konferensi', 
                                         help="Nama jurnal, konferensi, atau tempat publikasi")
    
    # Review details
    review_date = fields.Date('Tanggal Review', required=True)
    review_submission_date = fields.Date('Tanggal Submit untuk Review')
    review_completion_date = fields.Date('Tanggal Selesai Review')
    review_round = fields.Selection([
        ('1', 'Round 1'),
        ('2', 'Round 2'),
        ('3', 'Round 3'),
        ('final', 'Final Review'),
    ], string='Putaran Review', default='1')
    
    # Review method
    review_method = fields.Selection([
        ('single_blind', 'Single Blind'),
        ('double_blind', 'Double Blind'),
        ('open', 'Open Review'),
        ('post_publication', 'Post-Publication Review'),
    ], string='Metode Review', default='double_blind')
    
    # Status review
    review_status = fields.Selection([
        ('invited', 'Diundang'),
        ('in_progress', 'Sedang Review'),
        ('completed', 'Selesai'),
        ('declined', 'Ditolak/Dibatalkan'),
    ], string='Status Review', default='in_progress', required=True)
    
    # Review result
    review_result = fields.Selection([
        ('accept', 'Diterima (Accept)'),
        ('minor_revision', 'Revisi Minor'),
        ('major_revision', 'Revisi Mayor'),
        ('reject', 'Ditolak (Reject)'),
        ('conditional_accept', 'Diterima Bersyarat'),
    ], string='Hasil Review', help="Rekomendasi hasil review")
    
    review_score = fields.Float('Skor Review', help="Skor penilaian (jika ada)")
    
    # Review content
    review_focus_areas = fields.Text('Area Fokus Review', 
                                     help="Area yang menjadi fokus dalam review (metodologi, hasil, dll)")
    strengths = fields.Html('Kelebihan', help="Kelebihan dari karya yang direview", sanitize=False)
    weaknesses = fields.Html('Kelemahan', help="Kelemahan yang perlu diperbaiki", sanitize=False)
    recommendations = fields.Html('Rekomendasi', help="Rekomendasi untuk perbaikan", sanitize=False)
    reviewer_comments = fields.Html('Catatan Reviewer', help="Catatan atau komentar tambahan reviewer", sanitize=False)
    
    # Workload
    estimated_hours = fields.Float('Estimasi Waktu (jam)', help="Estimasi waktu yang dibutuhkan untuk review")
    actual_hours = fields.Float('Waktu Aktual (jam)', help="Waktu aktual yang digunakan untuk review")
    
    # Documentation
    document_url = fields.Char('URL Dokumen', help="Link ke dokumen/paper yang direview (jika tersedia online)")
    review_document = fields.Binary('Dokumen Review')
    review_document_filename = fields.Char('Nama File Dokumen')
    certificate_file = fields.Binary('Sertifikat Review', help="Upload sertifikat apresiasi sebagai reviewer")
    certificate_filename = fields.Char('Nama File Sertifikat')
    
    # Additional info
    keywords = fields.Text('Kata Kunci', help="Kata kunci/topik paper yang direview, pisahkan dengan koma")
    
    # Computed fields
    review_year = fields.Integer('Tahun Review', compute='_compute_review_year', store=True)
    review_duration_days = fields.Integer('Durasi Review (hari)', compute='_compute_review_duration', store=True)
    
    def _generate_slug_from_name(self, name):
        """Generate URL-friendly slug from name"""
        if not name:
            return ''
        import re
        # Convert to lowercase and replace special characters
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug_from_name(vals['name'])
        return super().create(vals_list)
    
    def write(self, vals):
        if 'name' in vals and not vals.get('slug'):
            vals['slug'] = self._generate_slug_from_name(vals['name'])
        return super().write(vals)
    
    @api.depends('review_date')
    def _compute_review_year(self):
        for record in self:
            if record.review_date:
                record.review_year = record.review_date.year
            else:
                record.review_year = datetime.now().year
    
    @api.depends('review_submission_date', 'review_completion_date')
    def _compute_review_duration(self):
        for record in self:
            if record.review_submission_date and record.review_completion_date:
                delta = record.review_completion_date - record.review_submission_date
                record.review_duration_days = delta.days
            else:
                record.review_duration_days = 0
    
    # Compute website URL untuk halaman khusus dengan SEO-friendly URL
    @api.depends('slug', 'blog_id')
    def _compute_website_url(self):
        for post in self:
            if post.id and post.blog_id and post.slug:
                post.website_url = f"/reviewer/detail/{post.slug}-{post.id}"
            elif post.id and post.blog_id:
                post.website_url = f"/reviewer/detail/{post.id}"
            else:
                post.website_url = ''
    
    def get_meta_title(self):
        """Get meta title for SEO"""
        return self.meta_title or self.name
    
    def get_meta_description(self):
        """Get meta description for SEO"""
        return self.meta_description or self.teaser or f"Aktivitas Review: {self.name}"
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'invited': 'badge-info',
            'in_progress': 'badge-warning',
            'completed': 'badge-success',
            'declined': 'badge-secondary',
        }
        return status_classes.get(self.review_status, 'badge-secondary')
    
    def get_result_badge_class(self):
        """Return CSS class for result badge"""
        result_classes = {
            'accept': 'badge-success',
            'minor_revision': 'badge-info',
            'major_revision': 'badge-warning',
            'reject': 'badge-danger',
            'conditional_accept': 'badge-primary',
        }
        return result_classes.get(self.review_result, 'badge-secondary')
