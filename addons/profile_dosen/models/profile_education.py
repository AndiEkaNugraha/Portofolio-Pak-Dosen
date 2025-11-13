# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProfileEducation(models.Model):
    _name = 'profile.education'
    _description = 'Riwayat Pendidikan'
    _order = 'end_year desc, start_year desc'
    
    profile_post_id = fields.Many2one('profile.post', 'Profile', ondelete='cascade')
    
    # Education details
    degree = fields.Selection([
        ('s3', 'S3 (Doktor)'),
        ('s2', 'S2 (Magister)'),
        ('s1', 'S1 (Sarjana)'),
        ('d4', 'D4'),
        ('d3', 'D3'),
        ('sma', 'SMA/SMK'),
    ], string='Jenjang', required=True)
    
    institution = fields.Char('Institusi/Universitas', required=True)
    faculty = fields.Char('Fakultas')
    major = fields.Char('Program Studi/Jurusan', required=True)
    
    start_year = fields.Integer('Tahun Mulai', required=True)
    end_year = fields.Integer('Tahun Selesai')
    is_current = fields.Boolean('Sedang Berjalan', default=False)
    
    gpa = fields.Float('IPK/GPA')
    gpa_scale = fields.Float('Skala IPK', default=4.0)
    
    country = fields.Char('Negara', default='Indonesia')
    city = fields.Char('Kota')
    
    # Thesis/Dissertation
    thesis_title = fields.Char('Judul Skripsi/Tesis/Disertasi')
    thesis_advisor = fields.Char('Pembimbing')
    
    # Additional info
    achievements = fields.Text('Prestasi/Penghargaan', help="Prestasi atau penghargaan yang diperoleh selama pendidikan")
    description = fields.Text('Deskripsi Tambahan')
    
    # Documents
    certificate_file = fields.Binary('Ijazah/Sertifikat')
    certificate_filename = fields.Char('Nama File')
    transcript_file = fields.Binary('Transkrip Nilai')
    transcript_filename = fields.Char('Nama File Transkrip')
    
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Active', default=True)
    
    @api.onchange('is_current')
    def _onchange_is_current(self):
        if self.is_current:
            self.end_year = False
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.degree.upper() if record.degree else ''} - {record.institution} ({record.start_year})"
            result.append((record.id, name))
        return result
