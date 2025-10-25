# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProdukBlog(models.Model):
    _name = 'produk.blog'
    _description = 'Kategori Produk Penelitian'
    _order = 'name'

    name = fields.Char('Nama Kategori', required=True, translate=True)
    subtitle = fields.Char('Sub Judul', translate=True, help="Deskripsi singkat kategori")
    
    # Technology focus
    technology_focus = fields.Selection([
        ('hardware', 'Hardware/Perangkat Keras'),
        ('software', 'Software/Aplikasi'),
        ('system', 'Sistem Terintegrasi'),
        ('material', 'Material/Bahan'),
        ('process', 'Proses/Metodologi'),
        ('service', 'Layanan/Service'),
        ('other', 'Lainnya')
    ], string='Fokus Teknologi', default='hardware')
    
    # Target application
    application_area = fields.Selection([
        ('industrial', 'Industri'),
        ('healthcare', 'Kesehatan'),
        ('education', 'Pendidikan'),
        ('agriculture', 'Pertanian'),
        ('energy', 'Energi'),
        ('transportation', 'Transportasi'),
        ('communication', 'Komunikasi'),
        ('environment', 'Lingkungan'),
        ('finance', 'Keuangan'),
        ('entertainment', 'Hiburan'),
        ('other', 'Lainnya')
    ], string='Bidang Aplikasi')
    
    # Scientific field
    scientific_field = fields.Selection([
        ('computer_science', 'Ilmu Komputer'),
        ('engineering', 'Teknik'),
        ('physics', 'Fisika'),
        ('chemistry', 'Kimia'),
        ('biology', 'Biologi'),
        ('medicine', 'Kedokteran'),
        ('agriculture', 'Pertanian'),
        ('social_science', 'Ilmu Sosial'),
        ('economics', 'Ekonomi'),
        ('management', 'Manajemen'),
        ('other', 'Lainnya')
    ], string='Bidang Keilmuan')
    
    description = fields.Html('Deskripsi', sanitize=False)
    active = fields.Boolean('Aktif', default=True)
    
    # Computed fields
    post_count = fields.Integer('Jumlah Produk', compute='_compute_post_count')
    
    @api.depends('produk_post_ids')
    def _compute_post_count(self):
        for record in self:
            record.post_count = len(record.produk_post_ids)
    
    # Inverse relation
    produk_post_ids = fields.One2many('produk.post', 'blog_id', string='Produk')
    
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.subtitle:
                name = f"{name} - {record.subtitle}"
            result.append((record.id, name))
        return result