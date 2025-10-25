# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class ProdukType(models.Model):
    _name = 'produk.type'
    _description = 'Jenis Produk'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Jenis Produk', required=True)
    code = fields.Char('Kode', required=True)
    description = fields.Text('Deskripsi')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)


class ProdukTechnology(models.Model):
    _name = 'produk.technology'
    _description = 'Teknologi Produk'
    _order = 'name'
    
    name = fields.Char('Nama Teknologi', required=True)
    code = fields.Char('Kode')
    category = fields.Selection([
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('ai_ml', 'AI/Machine Learning'),
        ('iot', 'Internet of Things'),
        ('blockchain', 'Blockchain'),
        ('robotics', 'Robotika'),
        ('biotech', 'Bioteknologi'),
        ('nanotech', 'Nanoteknologi'),
        ('material', 'Material Science'),
        ('energy', 'Teknologi Energi'),
        ('other', 'Lainnya')
    ], string='Kategori Teknologi')
    description = fields.Text('Deskripsi')
    active = fields.Boolean('Aktif', default=True)


class ProdukPost(models.Model):
    _name = 'produk.post'
    _description = 'Produk Penelitian'
    _order = 'development_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # Basic fields
    name = fields.Char('Nama Produk', required=True, translate=True, tracking=True)
    subtitle = fields.Char('Sub Judul', translate=True, help="Deskripsi singkat produk")
    blog_id = fields.Many2one('produk.blog', 'Kategori Produk', required=True, ondelete='cascade')
    
    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL friendly untuk website, akan dibuat otomatis jika kosong")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan nama produk jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan ringkasan jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
    
    # Content fields
    teaser = fields.Text('Ringkasan', help="Ringkasan singkat produk untuk preview dan website")
    content = fields.Html('Deskripsi Lengkap', help="Deskripsi detail produk", sanitize=False)
    
    # Website settings
    is_published = fields.Boolean('Tampilkan di Website', default=True, help="Centang untuk menampilkan produk ini di website portofolio")
    publication_date = fields.Datetime('Tanggal Publikasi Website', default=fields.Datetime.now)
    website_published = fields.Boolean('Published on Website', related='is_published', readonly=True)
    
    # Product classification
    produk_type_id = fields.Many2one('produk.type', 'Jenis Produk', required=True)
    technology_ids = fields.Many2many('produk.technology', 'produk_technology_rel', 'produk_id', 'technology_id', 'Teknologi yang Digunakan')
    
    # Development info
    development_date = fields.Date('Tanggal Mulai Pengembangan', required=True)
    completion_date = fields.Date('Tanggal Selesai Pengembangan')
    development_duration = fields.Integer('Durasi Pengembangan (bulan)', compute='_compute_development_duration', store=True)
    
    # Status and TRL
    development_status = fields.Selection([
        ('concept', 'Konsep/Ide'),
        ('design', 'Desain'),
        ('prototype', 'Prototype'),
        ('testing', 'Testing/Validasi'),
        ('pilot', 'Pilot/Uji Coba'),
        ('production', 'Produksi'),
        ('commercial', 'Komersialisasi'),
        ('discontinued', 'Dihentikan')
    ], string='Status Pengembangan', default='concept', required=True, tracking=True)
    
    trl_level = fields.Selection([
        ('1', 'TRL 1 - Basic principles observed'),
        ('2', 'TRL 2 - Technology concept formulated'),
        ('3', 'TRL 3 - Experimental proof of concept'),
        ('4', 'TRL 4 - Technology validated in lab'),
        ('5', 'TRL 5 - Technology validated in relevant environment'),
        ('6', 'TRL 6 - Technology demonstrated in relevant environment'),
        ('7', 'TRL 7 - System prototype demonstration'),
        ('8', 'TRL 8 - System complete and qualified'),
        ('9', 'TRL 9 - Actual system proven in operational environment')
    ], string='Technology Readiness Level', default='1', tracking=True)
    
    # Team and collaboration
    principal_investigator = fields.Char('Peneliti Utama', required=True, help="Nama peneliti utama/ketua tim")
    team_members = fields.Text('Anggota Tim', help="Daftar anggota tim, pisahkan dengan enter")
    partner_institutions = fields.Text('Institusi Mitra', help="Institusi atau perusahaan yang berkolaborasi")
    funding_source = fields.Char('Sumber Pendanaan')
    
    # Technical specifications
    technical_specs = fields.Html('Spesifikasi Teknis', help="Detail spesifikasi teknis produk", sanitize=False)
    technical_specifications = fields.Text('Spesifikasi Teknis (Alt)', help="Alias untuk spesifikasi teknis dalam format teks")
    innovation_points = fields.Html('Poin Inovasi', help="Keunggulan dan inovasi produk", sanitize=False)
    limitations = fields.Text('Keterbatasan', help="Keterbatasan atau tantangan produk")
    
    # Documentation
    product_image = fields.Binary('Foto Produk', help="Upload foto produk")
    product_filename = fields.Char('Nama File Foto')
    technical_drawing = fields.Binary('Gambar Teknis', help="Upload gambar teknis/blueprint")
    drawing_filename = fields.Char('Nama File Gambar Teknis')
    demo_video_url = fields.Char('URL Video Demo', help="Link ke video demonstrasi produk")
    documentation_file = fields.Binary('File Dokumentasi', help="Upload dokumentasi teknis (PDF)")
    documentation_filename = fields.Char('Nama File Dokumentasi')
    
    # Commercial potential
    target_market = fields.Text('Target Pasar', help="Deskripsi target pasar dan pengguna")
    market_potential = fields.Selection([
        ('low', 'Rendah'),
        ('medium', 'Sedang'),
        ('high', 'Tinggi'),
        ('very_high', 'Sangat Tinggi')
    ], string='Potensi Pasar', default='medium')
    
    estimated_market_size = fields.Char('Estimasi Ukuran Pasar')
    business_model = fields.Text('Model Bisnis', help="Rencana model bisnis untuk komersialisasi")
    competitive_advantage = fields.Text('Keunggulan Kompetitif')
    
    # IP and legal
    ip_status = fields.Selection([
        ('none', 'Tidak Ada'),
        ('planned', 'Direncanakan'),
        ('filed', 'Sudah Diajukan'),
        ('granted', 'Sudah Diterima'),
        ('published', 'Sudah Dipublikasi')
    ], string='Status Kekayaan Intelektual', default='none')
    
    patent_number = fields.Char('Nomor Paten/HKI')
    patent_title = fields.Char('Judul Paten/HKI')
    patent_date = fields.Date('Tanggal Paten/HKI')
    # related_hki_ids = fields.Many2many('hki.post', 'produk_hki_rel', 'produk_id', 'hki_id', 'HKI Terkait', help="HKI yang terkait dengan produk ini")  # Disabled - requires hki_paten module
    
    # Performance metrics
    performance_metrics = fields.Html('Metrik Kinerja', help="Data kinerja dan hasil testing", sanitize=False)
    awards_recognition = fields.Text('Penghargaan/Pengakuan', help="Penghargaan atau pengakuan yang diterima")
    publications = fields.Text('Publikasi Terkait', help="Paper atau publikasi yang berkaitan dengan produk")
    
    # Contact and links
    product_url = fields.Char('URL Produk', help="Link ke website/halaman produk")
    contact_email = fields.Char('Email Kontak')
    contact_phone = fields.Char('Telepon Kontak')
    
    # Computed fields
    display_team = fields.Char('Tim Lengkap', compute='_compute_display_team', store=True)
    age_in_months = fields.Integer('Usia Pengembangan (bulan)', compute='_compute_age_in_months')
    
    _sql_constraints = [
        ('slug_unique', 'unique(slug)', 'URL Slug harus unik untuk setiap produk!'),
    ]
    
    @api.depends('development_date', 'completion_date')
    def _compute_development_duration(self):
        for record in self:
            if record.development_date and record.completion_date:
                delta = record.completion_date - record.development_date
                record.development_duration = int(delta.days / 30)  # Approximate months
            else:
                record.development_duration = 0
    
    @api.depends('principal_investigator', 'team_members')
    def _compute_display_team(self):
        for record in self:
            team = record.principal_investigator or ''
            if record.team_members:
                if team:
                    team += f" (Lead), {record.team_members}"
                else:
                    team = record.team_members
            record.display_team = team
    
    @api.depends('development_date')
    def _compute_age_in_months(self):
        for record in self:
            if record.development_date:
                today = fields.Date.today()
                delta = today - record.development_date
                record.age_in_months = int(delta.days / 30)  # Approximate months
            else:
                record.age_in_months = 0
    
    @api.model
    def create(self, vals_list):
        # Handle both single dict and list of dicts
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            if vals.get('slug'):
                # Check if slug is already used
                existing_record = self.search([('slug', '=', vals['slug'])], limit=1)
                if existing_record:
                    # Auto-generate unique slug instead of raising error
                    vals['slug'] = self._generate_slug(vals.get('name', ''), exclude_id=None)
            elif vals.get('name'):
                vals['slug'] = self._generate_slug(vals['name'])
        
        records = super().create(vals_list)
        
        # Ensure slug uniqueness for newly created records
        for record in records:
            if record.slug:
                unique_slug = self._generate_slug(record.name, exclude_id=record.id)
                if unique_slug != record.slug:
                    record.slug = unique_slug
        
        return records
    
    def write(self, vals):
        if vals.get('slug'):
            # Validate slug uniqueness when manually edited
            existing_record = self.search([('slug', '=', vals['slug']), ('id', '!=', self.id)], limit=1)
            if existing_record:
                # Auto-generate unique slug instead of raising error
                vals['slug'] = self._generate_slug(vals.get('name', self.name), exclude_id=self.id)
        
        if not vals.get('slug') and vals.get('name'):
            vals['slug'] = self._generate_slug(vals['name'], exclude_id=self.id)
        elif vals.get('name') and not self.slug:
            vals['slug'] = self._generate_slug(vals['name'], exclude_id=self.id)
        return super().write(vals)
    
    def _generate_slug(self, name, exclude_id=None):
        """Generate URL-friendly slug from name, ensuring uniqueness"""
        import re
        base_slug = name.lower()
        base_slug = re.sub(r'[^\w\s-]', '', base_slug)
        base_slug = re.sub(r'[-\s]+', '-', base_slug).strip('-')
        
        # Ensure uniqueness
        slug = base_slug
        counter = 1
        domain = [('slug', '=', slug)]
        if exclude_id:
            domain.append(('id', '!=', exclude_id))
        
        while self.search(domain):
            slug = f"{base_slug}-{counter}"
            counter += 1
            domain = [('slug', '=', slug)]
            if exclude_id:
                domain.append(('id', '!=', exclude_id))
        
        return slug
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Enable search by team members and technology in name_search"""
        if not args:
            args = []
        
        domain = args[:]
        if name:
            domain += [
                '|', '|', '|', '|',
                ('name', operator, name),
                ('principal_investigator', operator, name),
                ('team_members', operator, name),
                ('subtitle', operator, name),
                ('meta_keywords', operator, name)
            ]
        
        return self.search(domain, limit=limit).name_get()
    
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.principal_investigator:
                name = f"{name} - {record.principal_investigator}"
            if record.development_date:
                name = f"{name} ({record.development_date.year})"
            result.append((record.id, name))
        return result
    
    @api.onchange('slug')
    def _onchange_slug(self):
        """Validate slug uniqueness in real-time"""
        if self.slug:
            # Check if slug is already used by other records
            exclude_id = self.id if self.id else None
            existing_record = self.search([('slug', '=', self.slug)] + ([('id', '!=', exclude_id)] if exclude_id else []), limit=1)
            if existing_record:
                return {
                    'warning': {
                        'title': 'Slug Duplikat',
                        'message': f"URL Slug '{self.slug}' sudah digunakan oleh produk '{existing_record.name}'. Sistem akan mengubahnya menjadi unik saat disimpan."
                    }
                }