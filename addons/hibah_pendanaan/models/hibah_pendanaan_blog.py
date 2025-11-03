# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class HibahPendanaanBlog(models.Model):
    _name = 'hibah.pendanaan.blog'
    _description = 'Kategori Hibah dan Pendanaan'
    _order = 'sequence, name'

    name = fields.Char('Nama Kategori', required=True, help="Contoh: Hibah Nasional, Hibah Internasional, Pendanaan Industri")
    
    # Relations
    hibah_pendanaan_post_ids = fields.One2many('hibah.pendanaan.post', 'blog_id', 'Hibah & Pendanaan')
    
    # Statistics
    post_count = fields.Integer('Jumlah Hibah', compute='_compute_post_count', store=True)
    
    # Display & SEO
    sequence = fields.Integer('Urutan', default=10)
    website_published = fields.Boolean('Dipublikasikan di Website', default=True)
    active = fields.Boolean('Aktif', default=True)

    
    @api.depends('hibah_pendanaan_post_ids')
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.hibah_pendanaan_post_ids)
    
    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            if self.search_count([('name', '=', record.name), ('id', '!=', record.id)]) > 0:
                raise UserError("Nama kategori sudah ada, silakan gunakan nama lain.")