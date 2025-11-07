# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MataKuliahBlog(models.Model):
    _name = 'mata_kuliah.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori Mata Kuliah'

    # Override untuk mata kuliah
    name = fields.Char('Nama Kategori Mata Kuliah', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)

    # Field khusus mata kuliah
    course_level = fields.Selection([
        ('undergraduate', 'Sarjana'),
        ('graduate', 'Magister'),
        ('doctoral', 'Doktor'),
        ('all', 'Semua Tingkat'),
    ], string='Tingkat Pendidikan', default='all', required=True)

    faculty = fields.Char('Fakultas/Program Studi', help="Fakultas atau program studi yang menawarkan mata kuliah ini")

    # Computed field for post count
    post_count = fields.Integer('Jumlah Mata Kuliah', compute='_compute_post_count')

    # Relasi ke mata kuliah
    blog_post_ids = fields.One2many('mata_kuliah.post', 'blog_id', string='Mata Kuliah')

    def _compute_post_count(self):
        for blog in self:
            blog.post_count = self.env['mata_kuliah.post'].search_count([('blog_id', '=', blog.id)])

    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(MataKuliahBlog, self)._compute_website_url()
        for blog in self:
            blog.website_url = f"/mata-kuliah/kategori/{blog.id}"

    @api.model
    def _get_default_domain(self):
        """Return default domain for course entries"""
        return [('blog_id.course_level', 'in', ['undergraduate', 'graduate', 'doctoral', 'all'])]