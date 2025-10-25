# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class BukuPost(models.Model):
    _name = 'buku.post'
    _description = 'Entri Buku'
    _order = 'publication_year desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # Basic fields
    name = fields.Char('Judul Buku', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul buku")
    blog_id = fields.Many2one('buku.blog', 'Kategori Buku', required=True, ondelete='cascade')
    
    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL friendly untuk website, akan dibuat otomatis jika kosong")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan judul buku jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan ringkasan jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
        
    # Content fields
    teaser = fields.Text('Ringkasan', help="Ringkasan singkat buku untuk preview dan website")
    content = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap buku", sanitize=False)
    
    # Publication fields 
    is_published = fields.Boolean('Tampilkan di Website', default=True, help="Centang untuk menampilkan buku ini di website portofolio")
    active = fields.Boolean('Active', default=True)
    website_published = fields.Boolean('Published on Website', related='is_published', readonly=True)
    
    # Audit fields
    create_date = fields.Datetime('Created on', readonly=True)
    write_date = fields.Datetime('Last Updated on', readonly=True)
    create_uid = fields.Many2one('res.users', 'Created by', readonly=True)
    write_uid = fields.Many2one('res.users', 'Last Updated by', readonly=True)
    
    # Field khusus Buku
    authors = fields.Char('Penulis/Pengarang', required=True, help="Nama penulis, pisahkan dengan koma jika lebih dari satu")
    co_authors = fields.Char('Co-Penulis', help="Nama co-penulis jika ada")
    editors = fields.Char('Editor', help="Nama editor buku")
    
    # Jenis Buku
    buku_type_id = fields.Many2one('buku.type', 'Jenis Buku', required=True)
    
    # Publication details
    publisher_id = fields.Many2one('book.publisher', 'Penerbit')
    publisher_name = fields.Char('Nama Penerbit', help="Isi manual jika penerbit tidak ada di database")
    publication_year = fields.Integer('Tahun Terbit', required=True)
    publication_month = fields.Selection([
        ('1', 'Januari'), ('2', 'Februari'), ('3', 'Maret'),
        ('4', 'April'), ('5', 'Mei'), ('6', 'Juni'),
        ('7', 'Juli'), ('8', 'Agustus'), ('9', 'September'),
        ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
    ], string='Bulan Terbit')
    publication_date = fields.Date('Tanggal Terbit')
    
    # Book identification
    isbn = fields.Char('ISBN', help="International Standard Book Number")
    issn = fields.Char('ISSN', help="International Standard Serial Number (untuk jurnal/majalah)")
    doi = fields.Char('DOI', help="Digital Object Identifier")
    
    # Physical details
    pages = fields.Integer('Jumlah Halaman')
    edition = fields.Char('Edisi', help="Contoh: Edisi ke-2, Revised Edition, dll")
    language = fields.Selection([
        ('id', 'Bahasa Indonesia'),
        ('en', 'English'),
        ('ar', 'العربية'),
        ('zh', '中文'),
        ('es', 'Español'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('ja', '日本語'),
        ('ko', '한국어'),
        ('other', 'Lainnya')
    ], string='Bahasa', default='id', required=True)
    other_language = fields.Char('Bahasa Lainnya', help="Isi jika memilih 'Lainnya'")
    
    # Visual content
    cover_image = fields.Binary('Cover Buku', help="Upload gambar cover buku")
    cover_filename = fields.Char('Nama File Cover')
    
    # External links
    book_url = fields.Char('Link Buku', help="Link ke buku online (Google Books, Amazon, toko buku, dll)")
    
    # Classification
    dewey_classification = fields.Char('Klasifikasi Dewey', help="Dewey Decimal Classification")
    subject = fields.Char('Subjek/Topik', help="Subjek utama buku")
    keywords = fields.Text('Kata Kunci', help="Kata kunci dipisahkan dengan koma")
    
    # Field untuk kategorisasi bidang keilmuan
    scientific_field = fields.Selection([
        ('computer_science', 'Ilmu Komputer'),
        ('engineering', 'Teknik'),
        ('mathematics', 'Matematika'),
        ('physics', 'Fisika'),
        ('biology', 'Biologi'),
        ('chemistry', 'Kimia'),
        ('medicine', 'Kedokteran'),
        ('social_science', 'Ilmu Sosial'),
        ('economics', 'Ekonomi'),
        ('education', 'Pendidikan'),
        ('arts', 'Seni & Desain'),
        ('literature', 'Sastra'),
        ('psychology', 'Psikologi'),
        ('management', 'Manajemen'),
        ('law', 'Hukum'),
        ('philosophy', 'Filsafat'),
        ('history', 'Sejarah'),
        ('geography', 'Geografi'),
        ('agriculture', 'Pertanian'),
        ('architecture', 'Arsitektur'),
        ('other', 'Lainnya'),
    ], string='Bidang Keilmuan')
    
    # Academic level
    academic_level = fields.Selection([
        ('elementary', 'SD/MI'),
        ('junior_high', 'SMP/MTs'),
        ('senior_high', 'SMA/MA/SMK'),
        ('undergraduate', 'S1/Diploma'),
        ('graduate', 'S2'),
        ('postgraduate', 'S3'),
        ('professional', 'Profesional'),
        ('general', 'Umum'),
    ], string='Tingkat Akademik')
    
    # Book status
    status = fields.Selection([
        ('published', 'Terbit'),
        ('in_press', 'Dalam Cetak'),
        ('submitted', 'Diserahkan ke Penerbit'),
        ('draft', 'Draft'),
    ], string='Status Buku', default='published', required=True)
    
    # Awards and recognition
    award_received = fields.Boolean('Mendapat Penghargaan')
    award_description = fields.Char('Deskripsi Penghargaan')
    
    # Sales/impact info (optional)
    citation_count = fields.Integer('Jumlah Sitasi', default=0)
    print_run = fields.Integer('Oplah Cetak', help="Jumlah eksemplar yang dicetak")
    
    # Computed fields
    display_authors = fields.Char('Penulis Lengkap', compute='_compute_display_authors', store=True)
    website_url = fields.Char('Website URL', compute='_compute_website_url')
    
    @api.depends('authors', 'co_authors')
    def _compute_display_authors(self):
        for record in self:
            authors = record.authors or ''
            if record.co_authors:
                authors += f", {record.co_authors}"
            record.display_authors = authors
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Auto generate slug if not provided
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug_from_name(vals['name'])
        return super().create(vals_list)
    
    def write(self, vals):
        # Auto generate slug if name changed but slug not provided
        if 'name' in vals and 'slug' not in vals:
            vals['slug'] = self._generate_slug_from_name(vals['name'])
        return super().write(vals)
    
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
    
    @api.depends('slug', 'name')
    def _compute_website_url(self):
        """Compute website URL for book detail page"""
        for book in self:
            if book.slug:
                book.website_url = f"/buku/detail/{book.slug}"
            else:
                book.website_url = f"/buku/detail/{book.id}"
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100):
        """Enable search by authors in name_search"""
        if args is None:
            args = []
        domain = args + [
            '|', '|', 
            ('name', operator, name),
            ('authors', operator, name),
            ('subtitle', operator, name)
        ]
        return self._search(domain, limit=limit, order=self._order)
    
    def name_get(self):
        """Custom name display format"""
        result = []
        for record in self:
            name = record.name
            if record.authors:
                name = f"{name} - {record.authors}"
            if record.publication_year:
                name = f"{name} ({record.publication_year})"
            result.append((record.id, name))
        return result
    
    def action_view_website(self):
        """Action to view book on website"""
        self.ensure_one()
        if not self.is_published:
            raise UserError('Buku belum dipublikasikan di website')
        
        # Generate website URL
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', 'http://localhost:8069')
        if self.slug:
            url = f"{base_url}/buku/detail/{self.slug}"
        else:
            url = f"{base_url}/buku/detail/{self.id}"
            
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }