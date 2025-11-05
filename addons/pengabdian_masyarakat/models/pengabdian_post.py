# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class PengabdianType(models.Model):
    _name = 'pengabdian.type'
    _description = 'Jenis Kegiatan Pengabdian'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Jenis Pengabdian', required=True)
    code = fields.Char('Kode', required=True)
    description = fields.Text('Deskripsi')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)


class PengabdianPartner(models.Model):
    _name = 'pengabdian.partner'
    _description = 'Mitra Kegiatan Pengabdian'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Mitra', required=True)
    partner_type = fields.Selection([
        ('institution', 'Institusi'),
        ('company', 'Perusahaan'),
        ('community', 'Masyarakat'),
        ('organization', 'Organisasi'),
        ('government', 'Pemerintah'),
        ('ngo', 'LSM/NGO'),
        ('other', 'Lainnya'),
    ], string='Jenis Mitra', required=True, default='institution')
    
    website_url = fields.Char('Website', help="URL website mitra")
    contact_person = fields.Char('Contact Person', help="Nama orang yang dapat dihubungi")
    contact_email = fields.Char('Email Kontak')
    contact_phone = fields.Char('Telepon Kontak')
    address = fields.Text('Alamat')
    description = fields.Text('Deskripsi', help="Deskripsi peran mitra dalam kegiatan")
    
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)
    
    # Relations
    pengabdian_post_ids = fields.Many2many('pengabdian.post', 'pengabdian_post_partner_rel', 
                                          'partner_id', 'post_id', string='Kegiatan Pengabdian')


class PengabdianPost(models.Model):
    _name = 'pengabdian.post'
    _description = 'Entri Kegiatan Pengabdian Masyarakat'
    _order = 'implementation_date desc, id desc'
    
    # Basic fields
    name = fields.Char('Judul Kegiatan Pengabdian', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul atau deskripsi singkat")
    blog_id = fields.Many2one('pengabdian.blog', 'Kategori Pengabdian', required=True, ondelete='cascade')
    
    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL friendly untuk website, akan dibuat otomatis jika kosong")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan judul kegiatan jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan ringkasan jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
        
    # Content fields
    teaser = fields.Text('Ringkasan', help="Ringkasan singkat kegiatan untuk preview dan website")
    content = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kegiatan pengabdian", sanitize=False)
    
    # Cover photo
    cover_image = fields.Binary('Foto Cover', attachment=True, help="Foto cover untuk kegiatan pengabdian")
    cover_image_filename = fields.Char('Nama File Cover')
    
    # Integration with hibah_pendanaan
    hibah_pendanaan_ids = fields.Many2many('hibah.pendanaan.post', 'pengabdian_hibah_rel', 
                                          'pengabdian_id', 'hibah_id', string='Sumber Hibah/Pendanaan', 
                                          help="Pilih hibah/pendanaan yang menjadi sumber dana kegiatan ini")
    
    # Publication fields 
    is_published = fields.Boolean('Tampilkan di Website', default=True, help="Centang untuk menampilkan kegiatan ini di website portofolio")
    active = fields.Boolean('Active', default=True)
    website_published = fields.Boolean('Published on Website', related='is_published', readonly=True)
    
    # Audit fields
    create_date = fields.Datetime('Created on', readonly=True)
    write_date = fields.Datetime('Last Updated on', readonly=True)
    create_uid = fields.Many2one('res.users', 'Created by', readonly=True)
    write_uid = fields.Many2one('res.users', 'Last Updated by', readonly=True)
    
    # Field khusus Kegiatan Pengabdian
    coordinator = fields.Char('Koordinator Kegiatan', required=True)
    team_members = fields.Text('Anggota Tim', help="Daftar anggota tim pelaksana")
    
    # Jenis kegiatan pengabdian
    pengabdian_type_id = fields.Many2one('pengabdian.type', 'Jenis Pengabdian', required=True)
    
    # Implementation details
    implementation_date = fields.Date('Tanggal Pelaksanaan', required=True)
    duration_days = fields.Integer('Durasi (hari)', help="Durasi kegiatan dalam hari")
    location = fields.Char('Lokasi Pelaksanaan', required=True)
    target_participants = fields.Char('Target Peserta', help="Jumlah dan jenis peserta target")
    
    # Important dates
    preparation_date = fields.Date('Tanggal Persiapan')
    completion_date = fields.Date('Tanggal Selesai')
    reporting_date = fields.Date('Tanggal Pelaporan')
    
    # Status kegiatan
    status = fields.Selection([
        ('planned', 'Direncanakan'),
        ('ongoing', 'Sedang Berlangsung'),
        ('completed', 'Selesai'),
        ('reported', 'Telah Dilaporkan'),
    ], string='Status Kegiatan', default='planned', required=True, help="Status pelaksanaan kegiatan pengabdian")
    
    # Partners and collaborators
    partner_ids = fields.Many2many('pengabdian.partner', 'pengabdian_post_partner_rel', 
                                  'post_id', 'partner_id', string='Mitra Kerjasama',
                                  help="Pilih mitra yang terlibat dalam kegiatan ini")
    
    # Target and objectives
    objectives = fields.Text('Tujuan Kegiatan', required=True)
    targets = fields.Text('Target Capaian', help="Target yang ingin dicapai")
    expected_outputs = fields.Text('Output yang Diharapkan')
    expected_outcomes = fields.Text('Outcome yang Diharapkan')
    
    # Implementation details
    methodology = fields.Text('Metode Pelaksanaan')
    activities = fields.Text('Kegiatan Utama', help="Deskripsi kegiatan yang dilakukan")
    resources_used = fields.Text('Sumber Daya yang Digunakan')
    
    # Results and impact
    actual_participants = fields.Char('Peserta Aktual', help="Jumlah peserta yang benar-benar terlibat")
    results_achieved = fields.Text('Hasil yang Dicapai')
    impact_assessment = fields.Text('Penilaian Dampak', help="Dampak yang dihasilkan terhadap masyarakat")
    sustainability_plan = fields.Text('Rencana Keberlanjutan')
    
    # Documentation
    documentation_links = fields.Char('Link Dokumentasi', help="URL ke dokumentasi kegiatan (foto, video, dll)")
    report_file = fields.Binary('File Laporan')
    report_filename = fields.Char('Nama File Laporan')
    
    # Evaluation and feedback
    participant_feedback = fields.Text('Feedback Peserta')
    self_evaluation = fields.Text('Evaluasi Mandiri')
    recommendations = fields.Text('Rekomendasi untuk Pengembangan')
    
    # Keywords and categorization
    keywords = fields.Text('Kata Kunci', help="Kata kunci dipisahkan dengan koma")
    thematic_area = fields.Char('Area TematiK', help="Area tematik kegiatan")
    
    # Computed fields
    implementation_year = fields.Integer('Tahun Pelaksanaan', compute='_compute_implementation_year', store=True)
    
    # Impact metrics
    beneficiaries_count = fields.Integer('Jumlah Penerima Manfaat', default=0)
    villages_reached = fields.Integer('Desa yang Terjangkau', default=0)
    sustainability_score = fields.Float('Skor Keberlanjutan', help="Skor 0-10 untuk keberlanjutan program")
    
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
    
    @api.depends('implementation_date')
    def _compute_implementation_year(self):
        for record in self:
            if record.implementation_date:
                record.implementation_year = record.implementation_date.year
            else:
                record.implementation_year = datetime.now().year
    
    # Override website URL untuk halaman khusus dengan SEO-friendly URL
    def _compute_website_url(self):
        super(PengabdianPost, self)._compute_website_url()
        for post in self:
            if post.id and post.blog_id and post.slug:
                post.website_url = f"/pengabdian/detail/{post.slug}-{post.id}"
            elif post.id and post.blog_id:
                post.website_url = f"/pengabdian/detail/{post.id}"
    
    def get_meta_title(self):
        """Get meta title for SEO"""
        return self.meta_title or self.name
    
    def get_meta_description(self):
        """Get meta description for SEO"""
        return self.meta_description or self.teaser or f"Kegiatan Pengabdian: {self.name}"
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'planned': 'badge-secondary',
            'ongoing': 'badge-warning',
            'completed': 'badge-success',
            'reported': 'badge-info',
        }
        return status_classes.get(self.status, 'badge-secondary')
    
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