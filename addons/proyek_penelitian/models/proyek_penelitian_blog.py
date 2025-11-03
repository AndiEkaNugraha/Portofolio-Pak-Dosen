# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ProyekPenelitianBlog(models.Model):
    _name = 'proyek.penelitian.blog'
    _description = 'Kategori Proyek Penelitian'
    _order = 'sequence, name'

    name = fields.Char('Nama Kategori', required=True, help="Contoh: Penelitian Dasar, Penelitian Terapan, Hibah Nasional")
    subtitle = fields.Char('Subjudul', help="Deskripsi singkat kategori proyek")
    description = fields.Text('Deskripsi', help="Deskripsi lengkap kategori proyek penelitian")
    
    # Research Type & Category
    research_type = fields.Selection([
        ('basic', 'Penelitian Dasar'),
        ('applied', 'Penelitian Terapan'),
        ('development', 'Penelitian Pengembangan'),
        ('collaborative', 'Penelitian Kolaboratif'),
        ('international', 'Penelitian Internasional'),
        ('industry', 'Kerjasama Industri'),
        ('government', 'Program Pemerintah'),
        ('other', 'Lainnya')
    ], string='Jenis Penelitian', required=True)
    
    funding_category = fields.Selection([
        ('national', 'Hibah Nasional'),
        ('international', 'Hibah Internasional'),
        ('industry', 'Pendanaan Industri'),
        ('internal', 'Dana Internal'),
        ('collaborative', 'Kolaboratif'),
        ('other', 'Lainnya')
    ], string='Kategori Pendanaan', required=True, default='national')
    
    # Institution & Information
    # institution = fields.Char('Institusi', help="Nama universitas atau institusi")  # REMOVED - not used in website
    # faculty = fields.Char('Fakultas/Departemen')  # REMOVED - not used in website
    # funding_agency = fields.Char('Lembaga Pendana', help="Contoh: Kemendikbud, BRIN, Kemenristek")  # REMOVED - not used in website
    
    # Relations
    proyek_penelitian_post_ids = fields.One2many('proyek.penelitian.post', 'blog_id', 'Proyek Penelitian')
    
    # Statistics
    post_count = fields.Integer('Jumlah Proyek', compute='_compute_post_count', store=True)
    # total_funding = fields.Float('Total Pendanaan (Rp)', help="Total nilai pendanaan semua proyek dalam kategori ini")  # REMOVED - not used in website
    
    # Display & SEO
    sequence = fields.Integer('Urutan', default=10)
    # is_published = fields.Boolean('Dipublikasikan', default=True)  # REMOVED - redundant with website_published
    website_published = fields.Boolean('Dipublikasikan di Website', default=True)
    active = fields.Boolean('Aktif', default=True)
    
    # Computed fields
    # display_name_full = fields.Char('Nama Lengkap', compute='_compute_display_name_full', store=True)  # REMOVED - not used in website
    
    # @api.depends('name', 'subtitle')  # REMOVED - method not needed
    # def _compute_display_name_full(self):  # REMOVED - method not needed
    #     for record in self:
    #         if record.subtitle:
    #             record.display_name_full = f"{record.name} - {record.subtitle}"
    #         else:
    #             record.display_name_full = record.name
    
    @api.depends('proyek_penelitian_post_ids')
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.proyek_penelitian_post_ids)
    
    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            if self.search_count([('name', '=', record.name), ('id', '!=', record.id)]) > 0:
                raise UserError("Nama kategori sudah ada, silakan gunakan nama lain.")