# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PengabdianBlog(models.Model):
    _name = 'pengabdian.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori Kegiatan Pengabdian'
    
    # Override untuk Pengabdian Masyarakat
    name = fields.Char('Nama Kategori Pengabdian', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kategori pengabdian")
    
    # Field khusus Pengabdian Masyarakat
    pengabdian_scope = fields.Selection([
        ('local', 'Lokal'),
        ('regional', 'Regional'),
        ('national', 'Nasional'),
        ('international', 'Internasional'),
    ], string='Cakupan Pengabdian', default='national', required=True)
    
    funding_source = fields.Selection([
        ('internal', 'Dana Internal'),
        ('external', 'Dana Eksternal'),
        ('community', 'Dana Masyarakat'),
        ('mixed', 'Campuran'),
    ], string='Sumber Dana')
    
    # Field untuk kategorisasi bidang pengabdian
    service_field = fields.Selection([
        ('education', 'Pendidikan'),
        ('health', 'Kesehatan'),
        ('agriculture', 'Pertanian'),
        ('environment', 'Lingkungan'),
        ('technology', 'Teknologi'),
        ('economy', 'Ekonomi'),
        ('social', 'Sosial'),
        ('culture', 'Budaya'),
        ('other', 'Lainnya'),
    ], string='Bidang Pengabdian')
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah Kegiatan', compute='_compute_post_count')
    
    # Relasi ke artikel pengabdian
    pengabdian_post_ids = fields.One2many('pengabdian.post', 'blog_id', string='Kegiatan Pengabdian')
    active = fields.Boolean('Active', default=True)
    
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.pengabdian_post_ids)
    
    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(PengabdianBlog, self)._compute_website_url()
        for blog in self:
            blog.website_url = f"/pengabdian/kategori/{blog.id}"
    
    @api.model
    def _get_default_domain(self):
        """Return default domain for pengabdian entries"""
        return [('blog_id.pengabdian_scope', 'in', ['local', 'regional', 'national', 'international'])]