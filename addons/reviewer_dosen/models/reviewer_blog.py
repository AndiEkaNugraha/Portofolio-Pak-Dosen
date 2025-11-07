# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReviewerBlog(models.Model):
    _name = 'reviewer.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori Aktivitas Review'
    
    # Override untuk Aktivitas Reviewer
    name = fields.Char('Nama Kategori Review', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kategori aktivitas review")
    
    # Field khusus Aktivitas Reviewer
    review_level = fields.Selection([
        ('local', 'Lokal'),
        ('national', 'Nasional'),
        ('regional', 'Regional (ASEAN/Asia)'),
        ('international', 'Internasional'),
    ], string='Level Review', default='national', required=True, 
       help="Tingkat atau cakupan review yang dilakukan")
    
    review_type = fields.Selection([
        ('journal', 'Jurnal Ilmiah'),
        ('book', 'Buku/Naskah'),
        ('research', 'Penelitian'),
        ('proposal', 'Proposal Penelitian'),
        ('conference', 'Artikel Konferensi'),
        ('thesis', 'Tugas Akhir/Disertasi'),
        ('grant', 'Hibah/Grant'),
        ('other', 'Lainnya'),
    ], string='Jenis Review', help="Jenis review yang dilakukan dalam kategori ini")
    
    # Field untuk kategorisasi bidang review
    review_field = fields.Selection([
        ('computer_science', 'Ilmu Komputer'),
        ('information_technology', 'Teknologi Informasi'),
        ('engineering', 'Teknik/Engineering'),
        ('science', 'Sains'),
        ('social_science', 'Ilmu Sosial'),
        ('humanities', 'Humaniora'),
        ('economics', 'Ekonomi'),
        ('education', 'Pendidikan'),
        ('health', 'Kesehatan'),
        ('agriculture', 'Pertanian'),
        ('multidisciplinary', 'Multidisiplin'),
        ('other', 'Lainnya'),
    ], string='Bidang Ilmu')
    
    # Indexing status
    indexing_status = fields.Selection([
        ('scopus', 'Scopus'),
        ('wos', 'Web of Science'),
        ('sinta', 'SINTA'),
        ('doaj', 'DOAJ'),
        ('non_indexed', 'Non-Indexed'),
        ('other', 'Lainnya'),
    ], string='Status Indexing', help="Status indexing untuk publikasi yang direview")
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah Aktivitas Review', compute='_compute_post_count')
    
    # Relasi ke aktivitas review
    reviewer_post_ids = fields.One2many('reviewer.post', 'blog_id', string='Aktivitas Review')
    active = fields.Boolean('Active', default=True)
    
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.reviewer_post_ids)
    
    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(ReviewerBlog, self)._compute_website_url()
        for blog in self:
            blog.website_url = f"/reviewer/kategori/{blog.id}"
    
    @api.model
    def _get_default_domain(self):
        """Return default domain for reviewer entries"""
        return [('blog_id.review_level', 'in', ['local', 'national', 'regional', 'international'])]
