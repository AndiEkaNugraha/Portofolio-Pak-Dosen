# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProfileBlog(models.Model):
    _name = 'profile.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori Profile Dosen'
    
    # Override untuk Profile Dosen
    name = fields.Char('Nama Kategori Profile', required=True, translate=True)
    subtitle = fields.Char('Deskripsi Kategori', translate=True)
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap kategori profile")
    
    # Field khusus Profile
    profile_type = fields.Selection([
        ('biography', 'Biografi'),
        ('education', 'Pendidikan'),
        ('work', 'Pekerjaan'),
        ('expertise', 'Keahlian'),
        ('award', 'Penghargaan'),
        ('general', 'Umum'),
    ], string='Jenis Profile', default='general', required=True)
    
    is_main_profile = fields.Boolean('Profile Utama', default=False, 
                                     help="Tandai sebagai kategori profile utama yang ditampilkan di halaman profil")
    
    # Computed field for post count
    post_count = fields.Integer('Jumlah Profile', compute='_compute_post_count')
    
    # Relasi ke profile post
    profile_post_ids = fields.One2many('profile.post', 'blog_id', string='Profile Items')
    active = fields.Boolean('Active', default=True)
    
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.profile_post_ids)
    
    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(ProfileBlog, self)._compute_website_url()
        for blog in self:
            blog.website_url = f"/profile/kategori/{blog.id}"
    
    @api.model
    def get_main_profile_blog(self):
        """Get main profile blog or create one if not exists"""
        blog = self.search([('is_main_profile', '=', True)], limit=1)
        if not blog:
            blog = self.create({
                'name': 'Profile Dosen',
                'subtitle': 'Profile Lengkap Dosen',
                'profile_type': 'biography',
                'is_main_profile': True,
            })
        return blog
