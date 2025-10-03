# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class HkiType(models.Model):
    _name = 'hki.type'
    _description = 'Jenis HKI'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Jenis HKI', required=True)
    code = fields.Char('Kode', required=True)
    description = fields.Text('Deskripsi')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)


class RegistrationOffice(models.Model):
    _name = 'registration.office'
    _description = 'Kantor Pendaftaran'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Kantor', required=True)
    code = fields.Char('Kode', required=True)
    country = fields.Char('Negara')
    website = fields.Char('Website')
    description = fields.Text('Deskripsi')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)


class HkiPost(models.Model):
    _name = 'hki.post'
    _description = 'Entri HKI dan Paten'
    _order = 'application_date desc, id desc'
    
    # Basic fields
    name = fields.Char('Judul HKI/Paten', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul atau deskripsi singkat")
    blog_id = fields.Many2one('hki.blog', 'Kategori HKI', required=True, ondelete='cascade')
    
    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL friendly untuk website, akan dibuat otomatis jika kosong")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan judul HKI jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan ringkasan jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
        
    # Content fields
    teaser = fields.Text('Ringkasan', help="Ringkasan singkat HKI untuk preview dan website")
    content = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap HKI/Paten", sanitize=False)
    
    # Publication fields 
    is_published = fields.Boolean('Tampilkan di Website', default=True, help="Centang untuk menampilkan HKI ini di website portofolio")
    active = fields.Boolean('Active', default=True)
    website_published = fields.Boolean('Published on Website', related='is_published', readonly=True)
    
    # Audit fields
    create_date = fields.Datetime('Created on', readonly=True)
    write_date = fields.Datetime('Last Updated on', readonly=True)
    create_uid = fields.Many2one('res.users', 'Created by', readonly=True)
    write_uid = fields.Many2one('res.users', 'Last Updated by', readonly=True)
    
    # Field khusus HKI dan Paten
    creators = fields.Char('Pencipta/Inventor', required=True)
    applicant = fields.Char('Pemohon/Pemegang Hak')
    
    # Jenis HKI
    hki_type_id = fields.Many2one('hki.type', 'Jenis HKI', required=True)
    
    # Registration details
    application_number = fields.Char('Nomor Permohonan')
    registration_number = fields.Char('Nomor Pendaftaran')
    certificate_number = fields.Char('Nomor Sertifikat')
    
    # Important dates
    application_date = fields.Date('Tanggal Permohonan', required=True)
    registration_date = fields.Date('Tanggal Pendaftaran')
    publication_date = fields.Date('Tanggal Publikasi')
    grant_date = fields.Date('Tanggal Pemberian')
    
    # Status HKI (untuk portofolio)
    status = fields.Selection([
        ('registered', 'Terdaftar'),
        ('granted', 'Diberikan'),
        ('published', 'Dipublikasikan'),
    ], string='Status HKI', default='registered', required=True, help="Status HKI yang telah diperoleh")
    
    # Protection details
    protection_period = fields.Integer('Masa Perlindungan (tahun)', help="Berapa tahun masa perlindungan")
    expiry_date = fields.Date('Tanggal Berakhir')
    renewal_date = fields.Date('Tanggal Perpanjangan')
    
    # Registration office
    registration_office_id = fields.Many2one('registration.office', 'Kantor Pendaftaran')
    
    registration_country = fields.Char('Negara Pendaftaran')
    
    # Classification
    ipc_classification = fields.Char('Klasifikasi IPC', help="International Patent Classification")
    nice_classification = fields.Char('Klasifikasi Nice', help="Nice Classification untuk Merek")
    locarno_classification = fields.Char('Klasifikasi Locarno', help="Locarno Classification untuk Desain Industri")
    
    # Technical details
    technical_field = fields.Char('Bidang Teknik')
    invention_area = fields.Text('Bidang Penemuan')
    keywords = fields.Text('Kata Kunci', help="Kata kunci dipisahkan dengan koma")
    
    # Claims (khusus untuk paten)
    claims_count = fields.Integer('Jumlah Klaim', help="Jumlah klaim untuk paten")
    independent_claims = fields.Integer('Klaim Bebas')
    dependent_claims = fields.Integer('Klaim Tidak Bebas')
    
    # Background art & prior art
    prior_art = fields.Text('Teknik Sebelumnya')
    advantages = fields.Text('Keunggulan/Keuntungan')
    
    # Commercial info
    commercialized = fields.Boolean('Sudah Dikomersialisasi')
    licensee = fields.Char('Penerima Lisensi')
    license_agreement = fields.Char('Perjanjian Lisensi')
    
    # Computed fields
    application_year = fields.Integer('Tahun Permohonan', compute='_compute_application_year', store=True)
    
    # Citation & impact metrics
    citations = fields.Integer('Jumlah Sitasi', default=0)
    family_patents = fields.Integer('Anggota Keluarga Paten', default=1)
    
    # Award/recognition
    award_received = fields.Boolean('Mendapat Penghargaan')
    award_description = fields.Char('Deskripsi Penghargaan')
    
    # Files & documents
    certificate_file = fields.Binary('File Sertifikat')
    certificate_filename = fields.Char('Nama File Sertifikat')
    patent_document = fields.Binary('Dokumen Paten/HKI')
    patent_filename = fields.Char('Nama File Dokumen')
    
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
    
    @api.depends('application_date')
    def _compute_application_year(self):
        for record in self:
            if record.application_date:
                record.application_year = record.application_date.year
            else:
                record.application_year = datetime.now().year
    

    
    # Override website URL untuk halaman khusus dengan SEO-friendly URL
    def _compute_website_url(self):
        super(HkiPost, self)._compute_website_url()
        for post in self:
            if post.id and post.blog_id and post.slug:
                post.website_url = f"/hki/detail/{post.slug}-{post.id}"
            elif post.id and post.blog_id:
                post.website_url = f"/hki/detail/{post.id}"
    
    def get_meta_title(self):
        """Get meta title for SEO"""
        return self.meta_title or self.name
    
    def get_meta_description(self):
        """Get meta description for SEO"""
        return self.meta_description or self.teaser or f"HKI/Paten: {self.name}"
    
    def get_meta_keywords(self):
        """Get meta keywords for SEO"""
        if self.meta_keywords:
            return self.meta_keywords
        keywords = []
        if self.creators:
            keywords.extend(self.creators.split(',')[:2])  # First 2 creators
        if self.hki_type:
            keywords.append(dict(self._fields['hki_type'].selection)[self.hki_type])
        if self.technical_field:
            keywords.append(self.technical_field)
        if self.registration_office:
            keywords.append(dict(self._fields['registration_office'].selection)[self.registration_office])
        return ', '.join(keywords) if keywords else ''
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'draft': 'badge-secondary',
            'applied': 'badge-info',
            'under_examination': 'badge-warning',
            'published': 'badge-primary',
            'granted': 'badge-success',
            'registered': 'badge-success',
            'rejected': 'badge-danger',
            'withdrawn': 'badge-dark',
            'expired': 'badge-dark',
            'abandoned': 'badge-dark',
        }
        return status_classes.get(self.status, 'badge-secondary')
    
    def get_hki_type_icon(self):
        """Return icon class for HKI type"""
        type_icons = {
            'copyright': 'fa-copyright',
            'patent': 'fa-lightbulb',
            'simple_patent': 'fa-lightbulb-o',
            'trademark': 'fa-trademark',
            'industrial_design': 'fa-paint-brush',
            'layout_design': 'fa-microchip',
            'plant_variety': 'fa-leaf',
            'trade_secret': 'fa-lock',
        }
        return type_icons.get(self.hki_type, 'fa-file')
    
    def get_protection_years_remaining(self):
        """Calculate remaining protection years"""
        if self.expiry_date:
            from datetime import date
            today = date.today()
            if self.expiry_date > today:
                delta = self.expiry_date - today
                return int(delta.days / 365.25)
        return 0
    
    def is_protection_active(self):
        """Check if protection is still active"""
        if self.status in ['granted', 'registered'] and self.expiry_date:
            from datetime import date
            return self.expiry_date > date.today()
        return False

    @api.depends('name')
    def _compute_slug(self):
        """Compute URL-friendly slug from name"""
        for record in self:
            if record.name:
                import re
                # Convert to lowercase and replace spaces/special chars with hyphens
                slug = re.sub(r'[^\w\s-]', '', record.name.lower())
                slug = re.sub(r'[-\s]+', '-', slug)
                record.slug = slug.strip('-')
            else:
                record.slug = False