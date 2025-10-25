# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BukuBlog(models.Model):
    _name = 'buku.blog'
    _description = 'Kategori Buku dan Karya Tulis'
    
    # Basic fields
    name = fields.Char('Nama Kategori Buku', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kategori buku")
    active = fields.Boolean('Active', default=True)
    
    # Field khusus Buku & Karya Tulis
    book_scope = fields.Selection([
        ('national', 'Nasional'),
        ('international', 'Internasional'),
        ('both', 'Nasional & Internasional'),
    ], string='Cakupan Publikasi', default='both', required=True)
    
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
        ('other', 'Lainnya'),
    ], string='Bidang Keilmuan')
    
    # Target pembaca
    target_audience = fields.Selection([
        ('undergraduate', 'Mahasiswa S1'),
        ('graduate', 'Mahasiswa S2/S3'),
        ('researcher', 'Peneliti'),
        ('professional', 'Profesional'),
        ('general', 'Umum'),
        ('children', 'Anak-anak'),
        ('teacher', 'Guru/Dosen'),
    ], string='Target Pembaca')
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah Buku', compute='_compute_post_count')
    
    # Relasi ke buku
    buku_post_ids = fields.One2many('buku.post', 'blog_id', string='Buku dan Karya Tulis')
    
    @api.depends('buku_post_ids')
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.buku_post_ids)