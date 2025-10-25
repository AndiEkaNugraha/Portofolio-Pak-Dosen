# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HkiBlog(models.Model):
    _name = 'hki.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori HKI dan Paten'
    
    # Override untuk HKI & Paten
    name = fields.Char('Nama Kategori HKI', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kategori HKI")
    
    # Field khusus HKI & Paten
    hki_scope = fields.Selection([
        ('national', 'Nasional'),
        ('international', 'Internasional'),
        ('both', 'Nasional & Internasional'),
    ], string='Cakupan HKI', default='both', required=True)
    
    registration_office = fields.Selection([
        ('kemenkumham', 'Kemenkumham RI'),
        ('uspto', 'USPTO (Amerika)'),
        ('epo', 'EPO (Eropa)'),
        ('jpo', 'JPO (Jepang)'),
        ('kipo', 'KIPO (Korea)'),
        ('sipo', 'SIPO (China)'),
        ('wipo', 'WIPO (World)'),
        ('other', 'Lainnya'),
    ], string='Kantor Pendaftaran')
    
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
        ('arts', 'Seni &amp; Desain'),
        ('literature', 'Sastra'),
        ('other', 'Lainnya'),
    ], string='Bidang Keilmuan')
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah HKI', compute='_compute_post_count')
    
    # Relasi ke artikel HKI
    hki_post_ids = fields.One2many('hki.post', 'blog_id', string='HKI dan Paten')
    active = fields.Boolean('Active', default=True)
    
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.hki_post_ids)
    
    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(HkiBlog, self)._compute_website_url()
        for blog in self:
            blog.website_url = f"/hki/kategori/{blog.id}"
    
    @api.model
    def _get_default_domain(self):
        """Return default domain for HKI entries"""
        return [('blog_id.hki_scope', 'in', ['national', 'international', 'both'])]