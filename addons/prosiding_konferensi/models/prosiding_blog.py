# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProsidingBlog(models.Model):
    _name = 'prosiding.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori Prosiding Konferensi'
    
    # Override untuk prosiding konferensi
    name = fields.Char('Nama Kategori Konferensi', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kategori konferensi")
    
    # Field untuk publikasi website
    website_published = fields.Boolean('Published on Website', default=False, help="Apakah kategori ini dipublikasikan di website")
    
    # Field khusus prosiding konferensi
    conference_scope = fields.Selection([
        ('national', 'Nasional'),
        ('international', 'Internasional'),
        ('both', 'Nasional & Internasional'),
    ], string='Cakupan Konferensi', default='both', required=True)
    
    accreditation_body = fields.Selection([
        ('ieee', 'IEEE'),
        ('acm', 'ACM'),
        ('springer', 'Springer'),
        ('elsevier', 'Elsevier'),
        ('scopus', 'Scopus Indexed'),
        ('wos', 'Web of Science'),
        ('sinta', 'SINTA'),
        ('other', 'Lainnya'),
    ], string='Badan Akreditasi/Publisher')
    
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
        ('other', 'Lainnya'),
    ], string='Bidang Keilmuan')
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah Prosiding', compute='_compute_post_count')
    
    # Relasi ke artikel prosiding
    prosiding_post_ids = fields.One2many('prosiding.post', 'blog_id', string='Prosiding')
    
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.prosiding_post_ids)
    
    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(ProsidingBlog, self)._compute_website_url()
        for blog in self:
            blog.website_url = f"/prosiding/kategori/{blog.id}"
    
    @api.model
    def _get_default_domain(self):
        """Return default domain for proceeding entries"""
        return [('blog_id.conference_scope', 'in', ['national', 'international', 'both'])]
    
    def button_publish(self):
        """Publikasikan kategori prosiding ke website"""
        for record in self:
            record.website_published = True
        return True
    
    def button_unpublish(self):
        """Batalkan publikasi kategori prosiding dari website"""
        for record in self:
            record.website_published = False
        return True