# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import re


class BimbinganMahasiswa(models.Model):
    _name = 'bimbingan.mahasiswa'
    _description = 'Informasi Bimbingan Mahasiswa'
    _order = 'guidance_date desc, id desc'
    _inherit = ['mail.thread', 'website.published.mixin']

    # === INFORMASI DASAR ===
    name = fields.Char(string='Judul Bimbingan', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Deskripsi singkat bimbingan")
    
    # Mahasiswa yang dibimbing
    student_name = fields.Char(string='Nama Mahasiswa', required=True, help="Nama lengkap mahasiswa yang dibimbing")
    student_id = fields.Char(string='NIM/NPM', required=True, help="Nomor Induk Mahasiswa")
    student_email = fields.Char(string='Email Mahasiswa', help="Email kontak mahasiswa")
    student_phone = fields.Char(string='Telepon Mahasiswa', help="Nomor telepon/WhatsApp mahasiswa")
    
    # Program studi
    study_program = fields.Char(string='Program Studi', required=True, help="Program studi mahasiswa")
    academic_level = fields.Selection([
        ('s1', 'S1/Sarjana'),
        ('s2', 'S2/Magister'),
        ('s3', 'S3/Doktor'),
    ], string='Jenjang Akademik', required=True, default='s1')
    
    # === DETAIL BIMBINGAN ===
    guidance_type = fields.Selection([
        ('thesis', 'Skripsi/Tesis/Disertasi'),
        ('project', 'Proyek Akhir'),
        ('research', 'Riset/Penelitian'),
        ('academic', 'Bimbingan Akademik'),
        ('course', 'Bimbingan Mata Kuliah'),
        ('other', 'Lainnya'),
    ], string='Jenis Bimbingan', required=True, default='thesis')
    
    # Tema/Topik bimbingan
    topic = fields.Char(string='Tema/Topik Bimbingan', required=True, 
                       help="Tema atau topik utama bimbingan mahasiswa")
    description = fields.Html(string='Deskripsi Bimbingan', translate=True,
                             help="Penjelasan lengkap tentang bimbingan dan tujuannya")
    
    # Jadwal dan durasi
    guidance_date = fields.Date(string='Tanggal Bimbingan', required=True,
                               help="Tanggal dimulai bimbingan")
    estimated_completion = fields.Date(string='Target Selesai', 
                                      help="Target tanggal penyelesaian bimbingan")
    duration_months = fields.Integer(string='Durasi (bulan)', help="Durasi bimbingan estimasi dalam bulan")
    
    # Status bimbingan
    status = fields.Selection([
        ('active', 'Aktif'),
        ('completed', 'Selesai'),
        ('on_hold', 'On Hold'),
        ('pending', 'Pending'),
    ], string='Status Bimbingan', required=True, default='active',
       help="Status saat ini dari bimbingan mahasiswa")
    
    completion_percentage = fields.Integer(string='Persentase Penyelesaian (%)',
                                          help="Persentase progress bimbingan",
                                          default=0)
    
    # === OUTPUT/HASIL BIMBINGAN ===
    guidance_output = fields.Selection([
        ('thesis', 'Skripsi/Tesis/Disertasi'),
        ('paper', 'Makalah/Paper'),
        ('prototype', 'Prototipe/Prototype'),
        ('publication', 'Publikasi'),
        ('patent', 'Paten/HKI'),
        ('other', 'Lainnya'),
    ], string='Output Bimbingan', help="Hasil/output yang diharapkan dari bimbingan")
    
    guidance_notes = fields.Html(string='Catatan/Hasil Bimbingan',
                                help="Ringkasan hasil dan catatan penting dari sesi bimbingan")
    
    # === METRIK & STATISTIK ===
    meeting_count = fields.Integer(string='Jumlah Pertemuan', default=0, readonly=True,
                                  help="Total pertemuan bimbingan")
    total_hours = fields.Float(string='Total Jam Bimbingan', default=0.0,
                              help="Total durasi bimbingan dalam jam")
    
    # === SEO FIELDS ===
    slug = fields.Char(string='URL Slug', index=True, 
                      compute='_compute_slug', store=True,
                      help="URL friendly untuk website")
    meta_title = fields.Char(string='Meta Title', translate=True,
                            help="Judul untuk SEO")
    meta_description = fields.Text(string='Meta Description', translate=True,
                                  help="Deskripsi untuk SEO")
    meta_keywords = fields.Char(string='Meta Keywords',
                               help="Kata kunci untuk SEO, pisahkan dengan koma")
    
    # === WEBSITE & PUBLIKASI ===
    is_published = fields.Boolean(string='Tampilkan di Website', default=True,
                                 help="Centang untuk menampilkan bimbingan di website portofolio")
    website_published = fields.Boolean(related='is_published', readonly=True)
    website_url = fields.Char(string='Website URL', compute='_compute_website_url',
                             help="URL website untuk bimbingan ini")
    
    # === AUDIT FIELDS ===
    create_date = fields.Datetime(string='Created on', readonly=True)
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    
    # Relations
    active = fields.Boolean(default=True)
    
    # Computed fields
    @api.depends('name')
    def _compute_slug(self):
        """Generate URL-friendly slug from name"""
        for record in self:
            if record.name:
                slug = record.name.lower()
                slug = re.sub(r'[^\w\s-]', '', slug)
                slug = re.sub(r'[-\s]+', '-', slug)
                slug = slug.strip('-')
                record.slug = slug
            else:
                record.slug = False
    
    def _compute_website_url(self):
        """Generate website URL for guidance"""
        for record in self:
            if record.slug:
                record.website_url = f'/bimbingan-mahasiswa/{record.slug}'
            else:
                record.website_url = False
    
    # Methods untuk membuat SEO fields otomatis
    @api.model_create_multi
    def create(self, vals_list):
        """Override create untuk auto-generate SEO fields"""
        for vals in vals_list:
            if not vals.get('meta_title'):
                vals['meta_title'] = vals.get('name', '')
            if not vals.get('meta_description'):
                # Buat deskripsi otomatis dari subtitle
                subtitle = vals.get('subtitle', '')
                study_program = vals.get('study_program', '')
                topic = vals.get('topic', '')
                meta_desc = f"{subtitle or vals.get('name', '')} - {study_program}. {topic}"
                vals['meta_description'] = meta_desc[:160]  # Limited to 160 chars for SEO
            if not vals.get('meta_keywords'):
                # Generate keywords dari fields penting
                program = vals.get('study_program', '')
                guidance_type = vals.get('guidance_type', '')
                topic = vals.get('topic', '')
                vals['meta_keywords'] = f"{program}, {guidance_type}, {topic}, bimbingan mahasiswa"
        
        return super().create(vals_list)
    
    def write(self, vals):
        """Update SEO fields jika ada perubahan"""
        if 'name' in vals and not vals.get('meta_title'):
            vals['meta_title'] = vals['name']
        return super().write(vals)
    
    # Business logic
    def action_mark_completed(self):
        """Mark guidance as completed"""
        self.write({
            'status': 'completed',
            'completion_percentage': 100,
        })
    
    def action_mark_active(self):
        """Mark guidance as active"""
        self.write({'status': 'active'})
    
    def action_hold(self):
        """Put guidance on hold"""
        self.write({'status': 'on_hold'})
    
    def increment_meeting_count(self):
        """Increment meeting count"""
        self.meeting_count += 1
    
    # String representation
    def __str__(self):
        return f"{self.name} - {self.student_name}"
