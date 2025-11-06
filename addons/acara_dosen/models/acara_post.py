# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class AcaraPost(models.Model):
    _name = 'acara.post'
    _description = 'Entri Acara Dosen'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.published.mixin']
    _order = 'event_date desc, id desc'
    
    # Basic fields
    name = fields.Char('Judul Acara', required=True, translate=True, tracking=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul atau deskripsi singkat")
    blog_id = fields.Many2one('acara.blog', 'Kategori Acara', required=True, ondelete='cascade', tracking=True)
    
    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL friendly untuk website, akan dibuat otomatis jika kosong")
    website_meta_title = fields.Char(string="Meta Title")
    website_meta_description = fields.Text(string="Meta Description")
    website_meta_keywords = fields.Char(string="Meta Keywords")
    
    # Content fields
    teaser_text = fields.Text('Ringkasan', help="Ringkasan singkat acara untuk preview dan website")
    description_html = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap acara", sanitize=False)
    
    # Cover photo
    cover_image = fields.Binary('Foto Cover', attachment=True, help="Foto cover untuk acara")
    cover_image_filename = fields.Char('Nama File Cover')
    
    # Publication fields 
    active = fields.Boolean('Active', default=True)
    
    # Website URL
    website_url = fields.Char('Website URL', compute='_compute_website_url')
    
    # Field khusus Acara Dosen
    role = fields.Selection([
        ('speaker', 'Pembicara/Penyuluh'),
        ('moderator', 'Moderator'),
        ('jury', 'Juri/Penilai'),
        ('organizer', 'Penyelenggara'),
        ('participant', 'Peserta'),
        ('other', 'Lainnya'),
    ], string='Peran Dosen', required=True, default='speaker', tracking=True)
    
    # Jenis acara
    acara_type_id = fields.Many2one('acara.type', 'Jenis Acara', required=True, tracking=True)
    
    # Event details
    event_date = fields.Date('Tanggal Acara', required=True, index=True, tracking=True)
    event_end_date = fields.Date('Tanggal Selesai', help="Tanggal selesai acara jika berbeda dengan tanggal mulai")
    duration_hours = fields.Float('Durasi (jam)', help="Durasi acara dalam jam")
    location = fields.Char('Lokasi Acara', required=True)
    organizer = fields.Char('Penyelenggara', required=True)
    organizer_website = fields.Char('Website Penyelenggara', help="URL website resmi penyelenggara acara")
    co_organizer = fields.Char('Co-Organizer', help="Penyelenggara bersama jika ada")
    co_organizer_website = fields.Char('Website Co-Organizer', help="URL website resmi co-organizer")
    
    # Online/Offline
    event_format = fields.Selection([
        ('offline', 'Offline/Tatap Muka'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
    ], string='Format Acara', default='offline', required=True)
    
    # If online
    online_platform = fields.Char('Platform Online', help="Zoom, Google Meet, dll")
    meeting_link = fields.Char('Link Meeting')
    
    # Target audience
    target_audience = fields.Char('Target Peserta', help="Jumlah dan jenis peserta target")
    actual_participants = fields.Integer('Jumlah Peserta Aktual', default=0)
    
    # Status acara
    status = fields.Selection([
        ('upcoming', 'Akan Datang'),
        ('ongoing', 'Sedang Berlangsung'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ], string='Status Acara', default='upcoming', required=True, tracking=True, 
    help="Status acara akan otomatis berubah berdasarkan tanggal")
    
    # Additional info
    topics = fields.Text('Topik/Materi', help="Topik yang dibahas atau materi yang disampaikan")
    objectives = fields.Text('Tujuan Acara', required=True)
    outcomes = fields.Text('Hasil/Output', help="Hasil yang dicapai dari acara")
    
    # Documentation
    certificate_file = fields.Binary('File Sertifikat', attachment=True)
    certificate_filename = fields.Char('Nama File Sertifikat')
    documentation_links = fields.Char('Link Dokumentasi', help="URL ke dokumentasi acara (foto, video, dll)")
    presentation_file = fields.Binary('File Presentasi/Materi', attachment=True)
    presentation_filename = fields.Char('Nama File Presentasi')
    
    # Evaluation
    feedback = fields.Text('Feedback/Refleksi', help="Feedback dari peserta atau refleksi pribadi")
    impact = fields.Text('Dampak/Pengaruh', help="Dampak acara terhadap peserta atau komunitas")
    satisfaction_rating = fields.Selection([
        ('1', 'Sangat Kurang'),
        ('2', 'Kurang'),
        ('3', 'Cukup'),
        ('4', 'Baik'),
        ('5', 'Sangat Baik'),
    ], string='Rating Kepuasan', help="Rating kepuasan peserta")
    
    # Keywords
    keywords = fields.Text('Kata Kunci', help="Kata kunci dipisahkan dengan koma")
    
    # Computed fields
    event_year = fields.Integer('Tahun Acara', compute='_compute_event_year', store=True)
    duration_days = fields.Integer('Durasi (hari)', compute='_compute_duration_days', store=True, 
                                     help="Durasi acara dalam hari jika lebih dari 1 hari")
    
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
    
    @api.depends('event_date')
    def _compute_event_year(self):
        for record in self:
            if record.event_date:
                record.event_year = record.event_date.year
            else:
                record.event_year = datetime.now().year
    
    @api.depends('event_date', 'event_end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.event_date and record.event_end_date:
                delta = record.event_end_date - record.event_date
                record.duration_days = delta.days + 1
            else:
                record.duration_days = 1
    
    def _compute_website_url(self):
        """Compute website URL for detail page"""
        for post in self:
            if post.id and post.slug:
                post.website_url = f"/acara/detail/{post.slug}-{post.id}"
            elif post.id:
                post.website_url = f"/acara/detail/{post.id}"
            else:
                post.website_url = '/acara'
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'upcoming': 'badge-secondary',
            'ongoing': 'badge-warning',
            'completed': 'badge-success',
            'cancelled': 'badge-danger',
        }
        return status_classes.get(self.status, 'badge-secondary')