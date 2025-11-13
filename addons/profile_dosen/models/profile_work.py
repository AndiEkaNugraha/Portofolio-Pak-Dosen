# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProfileWork(models.Model):
    _name = 'profile.work'
    _description = 'Riwayat Pekerjaan/Jabatan'
    _order = 'end_date desc, start_date desc'
    
    profile_post_id = fields.Many2one('profile.post', 'Profile', ondelete='cascade')
    
    # Work details
    position = fields.Char('Jabatan/Posisi', required=True)
    institution = fields.Char('Institusi/Organisasi', required=True)
    department = fields.Char('Departemen/Unit')
    
    employment_type = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Kontrak'),
        ('freelance', 'Freelance'),
        ('internship', 'Magang'),
    ], string='Jenis Pekerjaan', default='full_time')
    
    work_type = fields.Selection([
        ('teaching', 'Dosen/Pengajar'),
        ('research', 'Peneliti'),
        ('administrative', 'Administratif'),
        ('management', 'Manajemen'),
        ('consultant', 'Konsultan'),
        ('other', 'Lainnya'),
    ], string='Tipe Pekerjaan')
    
    start_date = fields.Date('Tanggal Mulai', required=True)
    end_date = fields.Date('Tanggal Selesai')
    is_current = fields.Boolean('Masih Bekerja', default=False)
    
    location = fields.Char('Lokasi')
    country = fields.Char('Negara', default='Indonesia')
    
    # Job description
    description = fields.Html('Deskripsi Pekerjaan', help="Deskripsi tugas dan tanggung jawab")
    achievements = fields.Html('Pencapaian', help="Pencapaian atau kontribusi yang dicapai")
    
    # Skills used
    skills = fields.Text('Keterampilan yang Digunakan', help="Keterampilan atau teknologi yang digunakan, pisahkan dengan koma")
    
    # Documents
    appointment_letter = fields.Binary('Surat Keputusan/SK')
    appointment_letter_filename = fields.Char('Nama File SK')
    certificate_file = fields.Binary('Sertifikat/Bukti')
    certificate_filename = fields.Char('Nama File Sertifikat')
    
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Active', default=True)
    
    # Computed
    duration_months = fields.Integer('Durasi (bulan)', compute='_compute_duration', store=True)
    
    @api.depends('start_date', 'end_date', 'is_current')
    def _compute_duration(self):
        from dateutil.relativedelta import relativedelta
        from datetime import date
        
        for record in self:
            if record.start_date:
                end = record.end_date if record.end_date and not record.is_current else date.today()
                delta = relativedelta(end, record.start_date)
                record.duration_months = delta.years * 12 + delta.months
            else:
                record.duration_months = 0
    
    @api.onchange('is_current')
    def _onchange_is_current(self):
        if self.is_current:
            self.end_date = False
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.position} - {record.institution}"
            result.append((record.id, name))
        return result
