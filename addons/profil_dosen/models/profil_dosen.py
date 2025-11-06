# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ProfilDosen(models.Model):
    _name = 'profil.dosen'
    _description = 'Profil Dosen'
    _rec_name = 'nama_lengkap'

    # ==================== IDENTITAS ====================
    nama_lengkap = fields.Char('Nama Lengkap', required=True)
    nip = fields.Char('NIP/NIDN', help="Nomor Induk Pegawai atau Nomor Induk Dosen Nasional")
    email = fields.Char('Email', required=True)
    telepon = fields.Char('Nomor Telepon')
    
    # Status & Position
    jabatan = fields.Char('Jabatan', placeholder="Prof., Dr., Ir., M.Sc., etc.")
    posisi = fields.Char('Posisi Akademik', placeholder="Profesor, Lektor Kepala, etc.")
    departemen = fields.Char('Departemen/Prodi')
    institusi = fields.Char('Institusi', default='Universitas Teknologi Indonesia')
    
    # ==================== MEDIA ====================
    foto = fields.Image('Foto Profil', help="Upload foto profil dosen")
    cv_file = fields.Binary('File CV', attachment=True, help="Upload CV dalam format PDF")
    cv_filename = fields.Char('Nama File CV', compute='_compute_cv_filename', store=True)
    
    # ==================== INFORMASI UMUM ====================
    bio_singkat = fields.Text('Biografi Singkat', help="Deskripsi singkat maksimal 200 karakter")
    biografi = fields.Html('Biografi Lengkap', help="Penjelasan detail tentang dosen")
    visi_misi = fields.Html('Visi & Misi')
    
    # ==================== KEAHLIAN & RISET ====================
    bidang_keahlian = fields.Html('Bidang Keahlian', help="Daftar keahlian utama")
    minat_riset = fields.Html('Minat Riset', help="Area penelitian yang diminati")
    kata_kunci = fields.Char('Kata Kunci', help="Pisahkan dengan koma, contoh: AI, Machine Learning, Big Data")
    
    # ==================== PENDIDIKAN ====================
    pendidikan_s1 = fields.Char('Pendidikan S1', placeholder="S1 Teknik Informatika - Universitas Indonesia")
    pendidikan_s2 = fields.Char('Pendidikan S2', placeholder="S2 Teknik Informatika - ITB")
    pendidikan_s3 = fields.Char('Pendidikan S3', placeholder="S3 Computer Science - Stanford University")
    universitas_s1 = fields.Char('Universitas S1')
    universitas_s2 = fields.Char('Universitas S2')
    universitas_s3 = fields.Char('Universitas S3')
    tahun_lulus_s1 = fields.Integer('Tahun Lulus S1')
    tahun_lulus_s2 = fields.Integer('Tahun Lulus S2')
    tahun_lulus_s3 = fields.Integer('Tahun Lulus S3')
    
    # ==================== PENGALAMAN ====================
    pengalaman_kerja = fields.Html('Riwayat Pekerjaan', help="Daftar pengalaman kerja")
    tahun_pengalaman = fields.Integer('Tahun Pengalaman', compute='_compute_tahun_pengalaman')
    
    # ==================== PENCAPAIAN ====================
    total_publikasi = fields.Integer('Total Publikasi', default=0)
    total_proyek_riset = fields.Integer('Total Proyek Riset', default=0)
    total_paten = fields.Integer('Total Paten', default=0)
    h_index = fields.Integer('H-Index', default=0)
    total_sitasi = fields.Integer('Total Sitasi', default=0)
    
    penghargaan = fields.Html('Penghargaan & Pengakuan', help="Daftar penghargaan yang diterima")
    
    # ==================== MEDIA SOSIAL & ONLINE ====================
    linkedin_url = fields.Char('URL LinkedIn')
    google_scholar_url = fields.Char('URL Google Scholar')
    researchgate_url = fields.Char('URL ResearchGate')
    orcid_url = fields.Char('URL ORCID')
    website_url = fields.Char('Website Pribadi')
    
    # ==================== SEO & PUBLIKASI ====================
    slug = fields.Char('URL Slug', compute='_compute_slug', store=True, readonly=True)
    meta_title = fields.Char('Meta Title', help="SEO - Judul halaman")
    meta_description = fields.Char('Meta Description', help="SEO - Deskripsi halaman")
    meta_keywords = fields.Char('Meta Keywords', help="SEO - Kata kunci utama")
    
    # ==================== SISTEM ====================
    is_published = fields.Boolean('Publikasikan di Website', default=True)
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)
    
    created_at = fields.Datetime('Dibuat pada', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime('Diperbarui pada', compute='_compute_updated_at', store=True)

    # ==================== COMPUTE METHODS ====================
    def _compute_slug(self):
        """Generate URL slug dari nama"""
        for record in self:
            if record.nama_lengkap:
                import re
                name = record.nama_lengkap.lower()
                slug = re.sub(r'[^\w\s-]', '', name)
                slug = re.sub(r'[-\s]+', '-', slug)
                record.slug = slug.strip('-')
            else:
                record.slug = ''

    def _compute_cv_filename(self):
        """Ekstrak nama file dari CV binary"""
        for record in self:
            if record.cv_file:
                record.cv_filename = f"{record.nama_lengkap}_CV.pdf" if record.nama_lengkap else "CV.pdf"
            else:
                record.cv_filename = None

    def _compute_tahun_pengalaman(self):
        """Hitung tahun pengalaman dari pendidikan S1"""
        for record in self:
            if record.tahun_lulus_s1:
                record.tahun_pengalaman = datetime.now().year - record.tahun_lulus_s1
            else:
                record.tahun_pengalaman = 0

    def _compute_updated_at(self):
        """Update timestamp"""
        for record in self:
            record.updated_at = fields.Datetime.now()

    # ==================== ACTIONS ====================
    def action_publish(self):
        """Publikasikan profil ke website"""
        self.write({'is_published': True})

    def action_unpublish(self):
        """Unpublish profil dari website"""
        self.write({'is_published': False})

    def action_download_cv(self):
        """Action untuk download CV"""
        if not self.cv_file:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'File CV belum diunggah',
                    'type': 'warning',
                }
            }
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/cv_file/{self.cv_filename}',
            'target': 'new',
        }
