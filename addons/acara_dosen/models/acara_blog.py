# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcaraBlog(models.Model):
    _name = 'acara.blog'
    _description = 'Kategori Acara Dosen'
    _order = 'name'
    
    # Basic fields
    name = fields.Char('Nama Kategori Acara', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kategori acara")
    
    # Field khusus Acara Dosen
    acara_scope = fields.Selection([
        ('local', 'Lokal'),
        ('regional', 'Regional'),
        ('national', 'Nasional'),
        ('international', 'Internasional'),
    ], string='Cakupan Acara', default='national', required=True)
    
    event_type = fields.Selection([
        ('education', 'Pendidikan'),
        ('training', 'Pelatihan'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('conference', 'Konferensi'),
        ('jury', 'Juri/Penilai'),
        ('moderator', 'Moderator'),
        ('speaker', 'Pembicara'),
        ('other', 'Lainnya'),
    ], string='Jenis Acara Utama')
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah Acara', compute='_compute_post_count', store=True)
    
    # Relasi ke artikel acara
    acara_post_ids = fields.One2many('acara.post', 'blog_id', string='Acara Dosen')
    active = fields.Boolean('Active', default=True)
    
    # Website URL
    website_url = fields.Char('Website URL', compute='_compute_website_url')
    
    @api.depends('acara_post_ids')
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.acara_post_ids)
    
    def _compute_website_url(self):
        """Compute website URL for category page"""
        for blog in self:
            blog.website_url = f"/acara/kategori/{blog.id}"