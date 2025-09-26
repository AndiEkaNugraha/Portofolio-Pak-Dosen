# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JurnalBlog(models.Model):
    _name = 'jurnal.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori Jurnal Ilmiah'
    
    # Override untuk jurnal ilmiah
    name = fields.Char('Nama Kategori Jurnal', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    
    # Field khusus jurnal
    journal_scope = fields.Selection([
        ('national', 'Nasional'),
        ('international', 'Internasional'),
        ('both', 'Nasional & Internasional'),
    ], string='Cakupan Jurnal', default='both', required=True)
    
    accreditation_body = fields.Selection([
        ('sinta', 'SINTA'),
        ('scopus', 'Scopus'),
        ('wos', 'Web of Science'),
        ('doaj', 'DOAJ'),
        ('other', 'Lainnya'),
    ], string='Badan Akreditasi Utama')
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah Post', compute='_compute_post_count')
    
    # Relasi ke artikel jurnal
    blog_post_ids = fields.One2many('jurnal.post', 'blog_id', string='Artikel Jurnal')
    
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = self.env['jurnal.post'].search_count([('blog_id', '=', blog.id)])
    
    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(JurnalBlog, self)._compute_website_url()
        for blog in self:
            blog.website_url = f"/jurnal/kategori/{blog.id}"
    
    @api.model
    def _get_default_domain(self):
        """Return default domain for journal entries"""
        return [('blog_id.journal_scope', 'in', ['national', 'international', 'both'])]