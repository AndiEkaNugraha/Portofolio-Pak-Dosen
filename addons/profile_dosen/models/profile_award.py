# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProfileAward(models.Model):
    _name = 'profile.award'
    _description = 'Penghargaan & Pengakuan'
    _order = 'award_date desc, id desc'
    
    profile_post_id = fields.Many2one('profile.post', 'Profile', ondelete='cascade')
    
    # Award details
    name = fields.Char('Nama Penghargaan', required=True)
    award_type = fields.Selection([
        ('academic', 'Akademik'),
        ('research', 'Penelitian'),
        ('teaching', 'Pengajaran'),
        ('community_service', 'Pengabdian Masyarakat'),
        ('innovation', 'Inovasi'),
        ('professional', 'Profesional'),
        ('honorary', 'Kehormatan'),
        ('competition', 'Kompetisi'),
        ('other', 'Lainnya'),
    ], string='Jenis Penghargaan', required=True)
    
    issuer = fields.Char('Pemberi Penghargaan', required=True, help="Institusi atau organisasi pemberi penghargaan")
    award_date = fields.Date('Tanggal Penghargaan', required=True)
    award_year = fields.Integer('Tahun', compute='_compute_award_year', store=True)
    
    level = fields.Selection([
        ('internal', 'Internal/Institusi'),
        ('local', 'Lokal/Kota'),
        ('regional', 'Regional/Provinsi'),
        ('national', 'Nasional'),
        ('international', 'Internasional'),
    ], string='Tingkat Penghargaan', default='national')
    
    country = fields.Char('Negara', default='Indonesia')
    
    # Description
    description = fields.Html('Deskripsi', help="Deskripsi lengkap tentang penghargaan")
    achievement = fields.Text('Prestasi', help="Prestasi yang menjadi dasar penghargaan")
    
    # Certificate
    certificate_file = fields.Binary('Sertifikat/Piagam')
    certificate_filename = fields.Char('Nama File')
    certificate_image = fields.Binary('Foto Sertifikat', help="Foto sertifikat untuk ditampilkan di website")
    
    # Additional info
    certificate_number = fields.Char('Nomor Sertifikat')
    website_url = fields.Char('Website URL', help="Link ke website terkait penghargaan")
    
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Active', default=True)
    
    @api.depends('award_date')
    def _compute_award_year(self):
        for record in self:
            if record.award_date:
                record.award_year = record.award_date.year
            else:
                record.award_year = False
    
    def name_get(self):
        result = []
        for record in self:
            year = f" ({record.award_year})" if record.award_year else ""
            name = f"{record.name}{year}"
            result.append((record.id, name))
        return result
