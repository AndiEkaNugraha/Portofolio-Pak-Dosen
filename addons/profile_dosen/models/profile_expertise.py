# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProfileExpertise(models.Model):
    _name = 'profile.expertise'
    _description = 'Bidang Keahlian & Minat Riset'
    _order = 'sequence, name'
    
    profile_post_id = fields.Many2one('profile.post', 'Profile', ondelete='cascade')
    
    # Expertise details
    name = fields.Char('Nama Keahlian/Minat', required=True)
    expertise_type = fields.Selection([
        ('research_interest', 'Minat Riset'),
        ('expertise', 'Bidang Keahlian'),
        ('skill', 'Keterampilan'),
        ('certification', 'Sertifikasi'),
        ('specialization', 'Spesialisasi'),
    ], string='Tipe', required=True, default='research_interest')
    
    category = fields.Selection([
        ('computer_science', 'Ilmu Komputer'),
        ('information_technology', 'Teknologi Informasi'),
        ('artificial_intelligence', 'Kecerdasan Buatan'),
        ('data_science', 'Ilmu Data'),
        ('software_engineering', 'Rekayasa Perangkat Lunak'),
        ('network_security', 'Jaringan & Keamanan'),
        ('multimedia', 'Multimedia'),
        ('information_systems', 'Sistem Informasi'),
        ('engineering', 'Teknik/Engineering'),
        ('science', 'Sains'),
        ('mathematics', 'Matematika'),
        ('education', 'Pendidikan'),
        ('management', 'Manajemen'),
        ('other', 'Lainnya'),
    ], string='Kategori')
    
    proficiency_level = fields.Selection([
        ('beginner', 'Pemula'),
        ('intermediate', 'Menengah'),
        ('advanced', 'Lanjut'),
        ('expert', 'Ahli'),
    ], string='Tingkat Keahlian', default='intermediate')
    
    years_of_experience = fields.Integer('Tahun Pengalaman')
    
    # Description
    description = fields.Html('Deskripsi', help="Deskripsi detail tentang keahlian atau minat riset")
    
    # Related keywords
    keywords = fields.Text('Kata Kunci', help="Kata kunci terkait, pisahkan dengan koma")
    
    # Certification (if any)
    certification_name = fields.Char('Nama Sertifikasi')
    certification_issuer = fields.Char('Penerbit Sertifikasi')
    certification_date = fields.Date('Tanggal Sertifikasi')
    certification_expiry = fields.Date('Tanggal Kadaluarsa')
    certification_file = fields.Binary('File Sertifikat')
    certification_filename = fields.Char('Nama File')
    
    # Publications/Projects count related to this expertise
    related_publications_count = fields.Integer('Jumlah Publikasi Terkait', 
                                                help="Jumlah publikasi yang terkait dengan keahlian ini")
    related_projects_count = fields.Integer('Jumlah Proyek Terkait',
                                            help="Jumlah proyek yang terkait dengan keahlian ini")
    
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Active', default=True)
    
    def name_get(self):
        result = []
        for record in self:
            expertise_type = dict(self._fields['expertise_type'].selection).get(record.expertise_type, '')
            name = f"{record.name} ({expertise_type})"
            result.append((record.id, name))
        return result
