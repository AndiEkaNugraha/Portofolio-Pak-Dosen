# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class MatakuliahPost(models.Model):
    _name = 'matakuliah.post'
    _description = 'Mata Kuliah'
    _inherit = ['mail.thread', 'website.published.mixin']
    
    name = fields.Char(string='Nama', required=True)
    blog_id = fields.Many2one('matakuliah.blog', string='Kategori Mata Kuliah', required=True, ondelete='cascade')
    _order = 'course_code'

    # ===== INFORMASI DASAR MATA KULIAH =====
    course_code = fields.Char(string='Kode Mata Kuliah', required=True, size=32, index=True)
    course_name = fields.Char(string='Nama Mata Kuliah', required=True, size=256)
    course_english_name = fields.Char(string='Nama Mata Kuliah (Inggris)', size=256)
    credits = fields.Integer(string='SKS (Satuan Kredit Semester)', default=3)
    course_type = fields.Selection([
        ('teori', 'Teori'),
        ('praktik', 'Praktik'),
        ('seminar', 'Seminar'),
        ('praktek_lapangan', 'Praktek Lapangan'),
        ('tugas_akhir', 'Tugas Akhir'),
    ], string='Jenis Mata Kuliah', default='teori')

    # ===== PERSYARATAN & DETAIL MATA KULIAH =====
    prerequisites = fields.Text(string='Prasyarat/Prerequisite')
    corequisites = fields.Text(string='Co-requisite')
    semester_offered = fields.Char(string='Semester Ditawarkan', size=64)
    status_course = fields.Selection([
        ('wajib', 'Wajib'),
        ('pilihan', 'Pilihan'),
        ('wajib_minat', 'Wajib Minat'),
    ], string='Status Mata Kuliah', default='wajib')

    # ===== TUJUAN PEMBELAJARAN =====
    course_objectives = fields.Html(string='Tujuan Pembelajaran Umum (TPU)')
    learning_outcomes = fields.Html(string='Capaian Pembelajaran (Learning Outcomes)')
    cpmk_text = fields.Html(string='Capaian Pembelajaran Mata Kuliah (CPMK)')

    # ===== DESKRIPSI & KONTEN =====
    course_description = fields.Html(string='Deskripsi Mata Kuliah')
    course_content = fields.Html(string='Rencana Materi Pembelajaran (Silabus)')
    topics_outline = fields.Html(string='Garis Besar Materi')
    detailed_content = fields.Html(string='Materi Detail/Slide')

    # ===== METODE & PENILAIAN =====
    learning_methods = fields.Html(string='Metode Pembelajaran')
    teaching_strategy = fields.Text(string='Strategi Pembelajaran')
    media_pembelajaran = fields.Text(string='Media Pembelajaran')
    
    # Penilaian
    assessment_methods = fields.Html(string='Metode Penilaian')
    assessment_components = fields.Html(string='Komponen Penilaian')
    grading_scale = fields.Html(string='Skala Penilaian')
    minimum_grade = fields.Selection([
        ('A', 'A (80+)'),
        ('B', 'B (70-79)'),
        ('C', 'C (60-69)'),
        ('D', 'D (50-59)'),
    ], string='Nilai Minimum', default='C')

    # ===== REFERENSI & SUMBER BELAJAR =====
    required_textbooks = fields.Html(string='Buku Referensi Wajib')
    recommended_books = fields.Html(string='Buku Referensi Tambahan')
    online_resources = fields.Html(string='Sumber Daya Online')
    learning_platform = fields.Char(string='Platform/LMS', size=128)
    course_website = fields.Char(string='Website Mata Kuliah', size=256)

    # ===== JADWAL & RUANG KELAS =====
    day_of_week = fields.Selection([
        ('monday', 'Senin'),
        ('tuesday', 'Selasa'),
        ('wednesday', 'Rabu'),
        ('thursday', 'Kamis'),
        ('friday', 'Jumat'),
        ('saturday', 'Sabtu'),
        ('sunday', 'Minggu'),
    ], string='Hari')
    start_time = fields.Float(string='Jam Mulai')
    end_time = fields.Float(string='Jam Berakhir')
    classroom = fields.Char(string='Ruang Kelas', size=128)
    building = fields.Char(string='Gedung', size=128)
    capacity = fields.Integer(string='Kapasitas Kelas')
    max_participants = fields.Integer(string='Maksimal Peserta')

    # ===== KONTAK & OFFICE HOURS =====
    instructor_email = fields.Char(string='Email Instruktur', size=128)
    instructor_phone = fields.Char(string='Telepon Instruktur', size=20)
    office_location = fields.Char(string='Lokasi Kantor', size=256)
    office_hours = fields.Html(string='Jam Konsultasi')
    consultation_methods = fields.Char(string='Metode Konsultasi (chat/email/tatap muka)', size=256)

    # ===== ASISTEN DOSEN =====
    teaching_assistants = fields.Html(string='Asisten Dosen')
    ta_contact_info = fields.Html(string='Kontak Asisten Dosen')

    # ===== KEBIJAKAN KELAS =====
    attendance_policy = fields.Html(string='Kebijakan Kehadiran')
    plagiarism_policy = fields.Html(string='Kebijakan Plagiarisme')
    classroom_policies = fields.Html(string='Tata Tertib Kelas')
    makeup_policy = fields.Html(string='Kebijakan Ujian Susulan')

    # ===== INFORMASI TAMBAHAN =====
    additional_info = fields.Html(string='Informasi Tambahan')
    course_syllabus_file = fields.Binary(string='File Silabus')
    course_syllabus_filename = fields.Char(string='Nama File Silabus')
    
    # ===== SEO OPTIMIZATION =====
    slug = fields.Char(string='URL Slug', required=True, index=True, unique=True)
    meta_title = fields.Char(string='Meta Title', size=160)
    meta_description = fields.Char(string='Meta Description', size=160)
    meta_keywords = fields.Char(string='Meta Keywords', size=256)
    og_image = fields.Binary(string='Open Graph Image')
    og_image_url = fields.Char(string='Open Graph Image URL', compute='_compute_og_image_url', store=True)

    # ===== SQL CONSTRAINTS =====
    _sql_constraints = [
        ('course_code_unique', 'unique(course_code)', 'Kode mata kuliah harus unik!'),
        ('slug_unique', 'unique(slug)', 'URL slug harus unik!'),
    ]

    @api.model
    def default_get(self, fields_list):
        """Set default values for new records"""
        res = super().default_get(fields_list)
        
        # Get or create default blog for matakuliah
        blog_model = self.env['matakuliah.blog']
        blog = blog_model.search([], limit=1)
        if not blog:
            # Create default blog if none exists
            blog = blog_model.create({
                'name': 'Mata Kuliah - Default',
                'program_studi': 'Program Studi',
                'jenis_program': 'regular'
            })
        
        if blog:
            res['blog_id'] = blog.id
        
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """Generate slug dan name otomatis jika tidak ada"""
        for vals in vals_list:
            if not vals.get('slug'):
                vals['slug'] = self._generate_slug(vals.get('course_code', 'course'))
            # name field harus ada (inherited dari blog.post)
            if not vals.get('name'):
                vals['name'] = vals.get('course_name', vals.get('course_code', 'Untitled'))
        return super().create(vals_list)

    def _generate_slug(self, text):
        """Generate URL-friendly slug"""
        import re
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug

    @api.depends('og_image')
    def _compute_og_image_url(self):
        """Compute OG image URL"""
        for record in self:
            if record.og_image:
                record.og_image_url = f'/web/image/matakuliah.post/{record.id}/og_image'
            else:
                record.og_image_url = False

    def _get_image_filename(self):
        """Get image filename for download"""
        if self.course_syllabus_filename:
            return self.course_syllabus_filename
        return f'silabus_{self.course_code}.pdf'
