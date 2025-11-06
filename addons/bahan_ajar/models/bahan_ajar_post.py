# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class BahanAjarPost(models.Model):
    _name = 'bahan.ajar.post'
    _description = 'Bahan Ajar / E-Learning'
    _inherit = ['mail.thread', 'website.published.mixin']
    _order = 'sequence, name'

    # === INFORMASI DASAR ===
    name = fields.Char(string='Judul Materi', required=True, translate=True)
    sequence = fields.Integer(string='Urutan', default=10)
    course_name = fields.Char(string='Mata Kuliah', required=True)
    description = fields.Html(string='Deskripsi Materi', translate=True)
    content_type = fields.Selection([
        ('pdf', 'File PDF'),
        ('video', 'Video'),
        ('link', 'Link/URL'),
        ('embed', 'Embedded Content'),
    ], string='Jenis Konten', required=True, default='pdf')

    # === FILE PDF ===
    pdf_file = fields.Binary(string='File PDF')
    pdf_filename = fields.Char(string='Nama File PDF')
    pdf_size = fields.Float(string='Ukuran File (MB)', compute='_compute_pdf_size', store=True)

    # === VIDEO ===
    video_url = fields.Char(string='URL Video')
    video_provider = fields.Selection([
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('other', 'Lainnya'),
    ], string='Platform Video', compute='_compute_video_provider', store=True)
    video_embed_code = fields.Html(string='Kode Embed Video', compute='_compute_video_embed', store=True)

    # === LINK/URL ===
    resource_url = fields.Char(string='URL Sumber')
    resource_type = fields.Selection([
        ('website', 'Website'),
        ('lms', 'Learning Management System'),
        ('repository', 'Repositori'),
        ('other', 'Lainnya'),
    ], string='Jenis Sumber', default='website')

    # === METADATA & TAGS ===
    topic = fields.Char(string='Topik/Bab', size=128)
    learning_objectives = fields.Text(string='Tujuan Pembelajaran')
    tags = fields.Char(string='Tags', help='Comma-separated tags')
    duration = fields.Float(string='Durasi (menit)', help='Estimasi waktu belajar')
    difficulty = fields.Selection([
        ('basic', 'Dasar'),
        ('intermediate', 'Menengah'),
        ('advanced', 'Lanjut'),
    ], string='Tingkat Kesulitan', default='basic')

    # === STATISTIK ===
    view_count = fields.Integer(string='Jumlah Dilihat', default=0)
    download_count = fields.Integer(string='Jumlah Diunduh', default=0)
    last_accessed = fields.Datetime(string='Terakhir Diakses')

    # === SEO ===
    website_url = fields.Char('Website URL', compute='_compute_website_url')
    slug = fields.Char(string='URL Slug', compute='_compute_slug', store=True)
    meta_title = fields.Char(string='Meta Title', translate=True)
    meta_description = fields.Char(string='Meta Description', translate=True)
    meta_keywords = fields.Char(string='Meta Keywords')

    @api.depends('pdf_file')
    def _compute_pdf_size(self):
        for record in self:
            if record.pdf_file:
                # Konversi ke MB
                record.pdf_size = len(record.pdf_file) / (1024 * 1024)
            else:
                record.pdf_size = 0

    @api.depends('video_url')
    def _compute_video_provider(self):
        for record in self:
            if not record.video_url:
                record.video_provider = False
            elif 'youtube.com' in record.video_url or 'youtu.be' in record.video_url:
                record.video_provider = 'youtube'
            elif 'vimeo.com' in record.video_url:
                record.video_provider = 'vimeo'
            else:
                record.video_provider = 'other'

    @api.depends('video_url', 'video_provider')
    def _compute_video_embed(self):
        for record in self:
            if not record.video_url or not record.video_provider:
                record.video_embed_code = False
                continue

            if record.video_provider == 'youtube':
                video_id = self._get_youtube_video_id(record.video_url)
                if video_id:
                    record.video_embed_code = f'''
                        <div class="ratio ratio-16x9">
                            <iframe src="https://www.youtube.com/embed/{video_id}" 
                                    frameborder="0" 
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                    allowfullscreen>
                            </iframe>
                        </div>
                    '''
            elif record.video_provider == 'vimeo':
                video_id = self._get_vimeo_video_id(record.video_url)
                if video_id:
                    record.video_embed_code = f'''
                        <div class="ratio ratio-16x9">
                            <iframe src="https://player.vimeo.com/video/{video_id}" 
                                    frameborder="0" 
                                    allow="autoplay; fullscreen; picture-in-picture" 
                                    allowfullscreen>
                            </iframe>
                        </div>
                    '''
            else:
                record.video_embed_code = False

    def _get_youtube_video_id(self, url):
        """Extract YouTube video ID from URL"""
        import re
        youtube_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(youtube_regex, url)
        return match.group(1) if match else None

    def _get_vimeo_video_id(self, url):
        """Extract Vimeo video ID from URL"""
        import re
        vimeo_regex = r'vimeo\.com\/(?:channels\/(?:\w+\/)?|groups\/[^\/]*\/videos\/|)(\d+)(?:|\/\?)'
        match = re.search(vimeo_regex, url)
        return match.group(1) if match else None

    @api.depends('name')
    def _compute_slug(self):
        """Generate URL slug from name"""
        for record in self:
            if record.name:
                record.slug = self._generate_slug(record.name)

    def _generate_slug(self, name):
        """Generate URL-friendly slug"""
        import re
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')

    def _compute_website_url(self):
        """Compute complete URL for website"""
        for record in self:
            record.website_url = f'/bahan-ajar/{record.slug}'

    def track_view(self):
        """Track when material is viewed"""
        self.ensure_one()
        self.write({
            'view_count': self.view_count + 1,
            'last_accessed': fields.Datetime.now()
        })

    def track_download(self):
        """Track when material is downloaded"""
        self.ensure_one()
        self.write({
            'download_count': self.download_count + 1,
            'last_accessed': fields.Datetime.now()
        })