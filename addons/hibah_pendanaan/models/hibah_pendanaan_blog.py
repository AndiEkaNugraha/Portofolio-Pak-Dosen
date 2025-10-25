# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class HibahPendanaanBlog(models.Model):
    _name = 'hibah.pendanaan.blog'
    _description = 'Kategori Hibah dan Pendanaan'
    _order = 'sequence, name'

    name = fields.Char('Nama Kategori', required=True, help="Contoh: Hibah Nasional, Hibah Internasional, Pendanaan Industri")
    subtitle = fields.Char('Subjudul', help="Deskripsi singkat kategori hibah")
    description = fields.Text('Deskripsi', help="Deskripsi lengkap kategori hibah dan pendanaan")
    
    # Funding Type & Category
    funding_type = fields.Selection([
        ('research_grant', 'Hibah Penelitian'),
        ('community_service', 'Hibah Pengabdian Masyarakat'),
        ('innovation_grant', 'Hibah Inovasi'),
        ('international_grant', 'Hibah Internasional'),
        ('industry_funding', 'Pendanaan Industri'),
        ('government_funding', 'Pendanaan Pemerintah'),
        ('internal_funding', 'Dana Internal'),
        ('collaborative_funding', 'Pendanaan Kolaboratif'),
        ('startup_grant', 'Hibah Startup'),
        ('other', 'Lainnya')
    ], string='Jenis Pendanaan', required=True)
    
    funding_level = fields.Selection([
        ('institutional', 'Tingkat Institusi'),
        ('national', 'Tingkat Nasional'),
        ('regional', 'Tingkat Regional'),
        ('international', 'Tingkat Internasional'),
        ('global', 'Tingkat Global')
    ], string='Tingkat Pendanaan', required=True, default='national')
    
    # Funding Agency
    funding_agency = fields.Char('Lembaga Pemberi Dana', help="Contoh: Kemendikbud, BRIN, Kemenristek, NSF, EU")
    agency_type = fields.Selection([
        ('government', 'Pemerintah'),
        ('private', 'Swasta'),
        ('international', 'Internasional'),
        ('ngo', 'NGO/Yayasan'),
        ('industry', 'Industri'),
        ('university', 'Universitas'),
        ('other', 'Lainnya')
    ], string='Jenis Lembaga')
    
    # Relations
    hibah_pendanaan_post_ids = fields.One2many('hibah.pendanaan.post', 'blog_id', 'Hibah & Pendanaan')
    
    # Statistics
    post_count = fields.Integer('Jumlah Hibah', compute='_compute_post_count', store=True)
    total_funding = fields.Float('Total Pendanaan (Rp)', help="Total nilai pendanaan semua hibah dalam kategori ini")
    average_funding = fields.Float('Rata-rata Pendanaan (Rp)', compute='_compute_average_funding', store=True)
    
    # Institution & Information
    institution = fields.Char('Institusi', help="Nama universitas atau institusi")
    faculty = fields.Char('Fakultas/Departemen')
    contact_person = fields.Char('Narahubung', help="PIC untuk kategori hibah ini")
    
    # Display & SEO
    sequence = fields.Integer('Urutan', default=10)
    is_published = fields.Boolean('Dipublikasikan', default=True)
    website_published = fields.Boolean('Dipublikasikan di Website', default=True)
    active = fields.Boolean('Aktif', default=True)
    
    # Computed fields
    display_name_full = fields.Char('Nama Lengkap', compute='_compute_display_name_full', store=True)
    
    @api.depends('name', 'subtitle')
    def _compute_display_name_full(self):
        for record in self:
            if record.subtitle:
                record.display_name_full = f"{record.name} - {record.subtitle}"
            else:
                record.display_name_full = record.name
    
    @api.depends('hibah_pendanaan_post_ids')
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.hibah_pendanaan_post_ids)
    
    @api.depends('hibah_pendanaan_post_ids.total_amount')
    def _compute_average_funding(self):
        for blog in self:
            if blog.hibah_pendanaan_post_ids:
                total = sum(post.total_amount for post in blog.hibah_pendanaan_post_ids)
                count = len(blog.hibah_pendanaan_post_ids)
                blog.average_funding = total / count if count > 0 else 0
            else:
                blog.average_funding = 0
    
    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            if self.search_count([('name', '=', record.name), ('id', '!=', record.id)]) > 0:
                raise UserError("Nama kategori sudah ada, silakan gunakan nama lain.")