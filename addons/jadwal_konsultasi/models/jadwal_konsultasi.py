# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta


class JadwalKonsultasi(models.Model):
    _name = 'jadwal.konsultasi'
    _description = 'Jadwal Konsultasi Mahasiswa'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.published.mixin']
    _order = 'sequence, hari_konsultasi, jam_mulai'

    # === INFORMASI DASAR ===
    name = fields.Char(string='Judul Jadwal', required=True, translate=True, help='Judul jadwal konsultasi')
    description = fields.Html(string='Deskripsi/Catatan', translate=True, help='Catatan tambahan tentang jadwal konsultasi')
    sequence = fields.Integer(string='Urutan', default=10)
    
    # === JADWAL & WAKTU ===
    hari_konsultasi = fields.Selection([
        ('0', 'Senin'),
        ('1', 'Selasa'),
        ('2', 'Rabu'),
        ('3', 'Kamis'),
        ('4', 'Jumat'),
        ('5', 'Sabtu'),
        ('6', 'Minggu'),
    ], string='Hari Konsultasi', required=True)
    
    jam_mulai = fields.Float(string='Jam Mulai', required=True, help='Format: 14.5 untuk 14:30')
    jam_selesai = fields.Float(string='Jam Selesai', required=True, help='Format: 15.5 untuk 15:30')
    durasi_slot = fields.Float(string='Durasi Slot (menit)', default=30, help='Durasi waktu per sesi konsultasi')
    
    # === LOKASI ===
    tipe_lokasi = fields.Selection([
        ('ruangan', 'Ruangan/Fisik'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid (Ruangan + Online)'),
    ], string='Tipe Lokasi', required=True, default='ruangan')
    
    lokasi_ruangan = fields.Char(string='Ruangan', help='Nama/nomor ruangan untuk konsultasi fisik')
    lokasi_online = fields.Char(string='Link Online', help='Link untuk konsultasi online (Zoom, Meet, dll)')
    
    # === JENIS KONSULTASI ===
    jenis_konsultasi = fields.Selection([
        ('akademik', 'Akademik'),
        ('penelitian', 'Penelitian'),
        ('skripsi', 'Bimbingan Skripsi'),
        ('karir', 'Konsultasi Karir'),
        ('mentor', 'Mentoring'),
        ('umum', 'Umum/Lainnya'),
    ], string='Jenis Konsultasi', required=True, default='akademik')
    
    # === KAPASITAS & KUOTA ===
    kapasitas_maksimal = fields.Integer(string='Kapasitas Maksimal', default=1, help='Jumlah mahasiswa per slot')
    peserta_terdaftar = fields.Integer(string='Peserta Terdaftar', compute='_compute_peserta_terdaftar', store=True)
    kuota_tersedia = fields.Integer(string='Kuota Tersedia', compute='_compute_kuota_tersedia', store=True)
    
    # === SYARAT & KETENTUAN ===
    syarat_konsultasi = fields.Text(string='Syarat/Ketentuan', help='Syarat peserta atau persiapan sebelum konsultasi')
    persiapan_mahasiswa = fields.Text(string='Persiapan Mahasiswa', help='Yang perlu disiapkan mahasiswa')
    
    # === METADATA ===
    slug = fields.Char(string='Slug URL', compute='_compute_slug', store=True, translate=False)
    website_url = fields.Char(string='Website URL', compute='_compute_website_url', store=True)
    
    # === STATUS ===
    is_active = fields.Boolean(string='Jadwal Aktif', default=True)
    tanggal_dibuat = fields.Datetime(string='Tanggal Dibuat', default=fields.Datetime.now, readonly=True)
    tanggal_diubah = fields.Datetime(string='Tanggal Diubah', default=fields.Datetime.now, readonly=True)
    
    # === STATISTIK ===
    view_count = fields.Integer(string='Jumlah Dilihat', default=0)
    
    @api.depends('name')
    def _compute_slug(self):
        """Generate slug dari name"""
        for record in self:
            if record.name:
                # Convert to lowercase, replace spaces with dash
                slug = record.name.lower().replace(' ', '-')
                # Remove special characters
                slug = ''.join(c for c in slug if c.isalnum() or c == '-')
                record.slug = slug
            else:
                record.slug = ''
    
    @api.depends('slug')
    def _compute_website_url(self):
        """Generate website URL"""
        for record in self:
            if record.slug:
                record.website_url = f'/jadwal-konsultasi/{record.slug}'
            else:
                record.website_url = ''
    
    @api.depends('kapasitas_maksimal', 'peserta_terdaftar')
    def _compute_kuota_tersedia(self):
        """Hitung kuota yang masih tersedia"""
        for record in self:
            record.kuota_tersedia = max(0, record.kapasitas_maksimal - record.peserta_terdaftar)
    
    def _compute_peserta_terdaftar(self):
        """Hitung jumlah peserta terdaftar (stub untuk integrasi booking)"""
        for record in self:
            record.peserta_terdaftar = 0  # TODO: Integrate with booking model
    
    def track_view(self):
        """Track view count"""
        self.view_count += 1
    
    @api.model
    def default_get(self, fields_list):
        """Set default values ketika create baru"""
        defaults = super().default_get(fields_list)
        defaults.update({
            'hari_konsultasi': '0',  # Senin
            'jam_mulai': 14.0,
            'jam_selesai': 17.0,
            'kapasitas_maksimal': 5,
        })
        return defaults
    
    def format_jam(self, jam_float):
        """Convert float jam ke format HH:MM"""
        jam = int(jam_float)
        menit = int((jam_float - jam) * 60)
        return f"{jam:02d}:{menit:02d}"
    
    def get_jam_mulai_display(self):
        """Get formatted jam mulai"""
        return self.format_jam(self.jam_mulai)
    
    def get_jam_selesai_display(self):
        """Get formatted jam selesai"""
        return self.format_jam(self.jam_selesai)
    
    def get_hari_display(self):
        """Get nama hari"""
        hari_names = {
            '0': 'Senin',
            '1': 'Selasa',
            '2': 'Rabu',
            '3': 'Kamis',
            '4': 'Jumat',
            '5': 'Sabtu',
            '6': 'Minggu',
        }
        return hari_names.get(self.hari_konsultasi, '')
    
    def is_kuota_penuh(self):
        """Check apakah kuota sudah penuh"""
        return self.kuota_tersedia <= 0
    
    def is_available_now(self):
        """Check apakah jadwal tersedia hari ini"""
        from datetime import datetime
        today_weekday = str(datetime.now().weekday())
        return self.hari_konsultasi == today_weekday and self.is_active and not self.is_kuota_penuh()
