# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class HibahPendanaanPost(models.Model):
    _name = 'hibah.pendanaan.post'
    _description = 'Hibah dan Pendanaan'
    _order = 'start_date desc, id desc'

    # Basic Information
    name = fields.Char('Judul Hibah/Pendanaan', required=True)
    subtitle = fields.Char('Subjudul/Tagline', help="Tagline atau deskripsi singkat hibah")
    blog_id = fields.Many2one('hibah.pendanaan.blog', 'Kategori', required=True, ondelete='cascade')
    
    # Grant Details
    grant_number = fields.Char('Nomor Hibah', help="Nomor kontrak/SK hibah")
    grant_scheme = fields.Char('Skema Hibah', help="Nama skema hibah, contoh: Hibah Penelitian Dasar, PKM, dll")
    
    # Timeline & Status
    start_date = fields.Date('Tanggal Mulai', required=True)
    end_date = fields.Date('Tanggal Selesai')
    duration_months = fields.Integer('Durasi (Bulan)', compute='_compute_duration', store=True)
    status = fields.Selection([
        ('proposal', 'Tahap Proposal'),
        ('approved', 'Disetujui'),
        ('active', 'Sedang Berjalan'),
        ('completed', 'Selesai'),
        ('suspended', 'Ditunda'),
        ('cancelled', 'Dibatalkan'),
        ('extended', 'Diperpanjang')
    ], string='Status Hibah', required=True, default='proposal')
    
    # Funding Information
    funding_agency = fields.Char('Lembaga Pemberi Dana', required=True)
    funding_source = fields.Char('Sumber Dana', help="Detail sumber dana, contoh: APBN, APBD, Swasta")
    total_amount = fields.Float('Total Anggaran (Rp)', required=True)
    disbursed_amount = fields.Float('Dana Dicairkan (Rp)', help="Total dana yang sudah dicairkan")
    remaining_amount = fields.Float('Sisa Dana (Rp)', compute='_compute_remaining_amount', store=True)
    funding_year = fields.Char('Tahun Anggaran', help="Contoh: 2024, 2023-2025")
    
    # Contact Information (for hibah)
    contact_person = fields.Char('Narahubung Hibah', help="PIC untuk hibah ini")
    contact_email = fields.Char('Email Kontak')
    contact_phone = fields.Char('Telepon Kontak')
    
    # Budget Breakdown - One2many relation to flexible budget lines
    budget_line_ids = fields.One2many('hibah.budget.line', 'hibah_id', 'Rincian Anggaran')
    budget_total = fields.Float('Total dari Rincian', compute='_compute_budget_total', store=True)
    
    # Legacy budget fields (kept for compatibility, can be removed if not needed)
    personnel_cost = fields.Float('Biaya Personel (Rp)')
    equipment_cost = fields.Float('Biaya Peralatan (Rp)')
    material_cost = fields.Float('Biaya Bahan (Rp)')
    travel_cost = fields.Float('Biaya Perjalanan (Rp)')
    other_cost = fields.Float('Biaya Lainnya (Rp)')
    overhead_percentage = fields.Float('Overhead (%)')
    
    # Research Information (simplified - detailed research info in proyek)
    research_area = fields.Char('Bidang Penelitian', help="Area/bidang penelitian")
    research_focus = fields.Text('Fokus Penelitian', help="Deskripsi fokus penelitian hibah")
    keywords = fields.Char('Kata Kunci', help="Kata kunci hibah, pisahkan dengan koma")
    objectives = fields.Html('Tujuan Hibah', help="Tujuan dan target yang ingin dicapai")
    expected_outcomes = fields.Html('Luaran yang Diharapkan', help="Output dan outcome yang diharapkan")
    
    # Grant Application Information
    eligibility_criteria = fields.Html('Kriteria Kelayakan', help="Kriteria penerima hibah")
    application_requirements = fields.Html('Persyaratan Aplikasi', help="Dokumen dan persyaratan yang dibutuhkan")
    application_deadline = fields.Date('Batas Waktu Pendaftaran', help="Deadline pengajuan proposal")
    reporting_requirements = fields.Html('Kebutuhan Pelaporan', help="Jenis dan jadwal laporan yang diperlukan")
    
    # Documentation & Reporting - File Uploads
    interim_reports = fields.Binary('Laporan Kemajuan', help="Upload file laporan kemajuan", attachment=True)
    interim_reports_filename = fields.Char('Nama File Laporan Kemajuan')
    
    final_report = fields.Binary('Laporan Akhir', help="Upload file laporan akhir", attachment=True)
    final_report_filename = fields.Char('Nama File Laporan Akhir')
    
    financial_reports = fields.Binary('Laporan Keuangan', help="Upload file laporan keuangan", attachment=True)
    financial_reports_filename = fields.Char('Nama File Laporan Keuangan')
    
    audit_results = fields.Html('Hasil Audit', help="Hasil audit jika ada")
    
    # Removed duplicate fields that should be in proyek:
    # - partner_institutions, industry_partners, international_collaboration, international_partners
    # - phd_students, master_students, undergrad_students, research_assistants, external_experts
    # - publications, patents_ip, prototypes, conference_presentations, awards_recognition
    # - social_impact, economic_impact, environmental_impact, sustainability_plan
    # - milestone_achieved, current_activities, challenges_faced, next_steps
    # These are research outputs that belong to the project, not the grant itself
    
    # Content & Description
    teaser = fields.Text('Ringkasan Singkat', help="Deskripsi singkat untuk preview")
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi detail hibah/pendanaan")
    background = fields.Html('Latar Belakang', help="Latar belakang dan urgensi hibah")
    terms_conditions = fields.Html('Syarat & Ketentuan', help="Syarat dan ketentuan hibah")
    
    # Contact & External Links (for public)
    project_website = fields.Char('Website Hibah', help="Website informasi hibah jika ada")
    
    # Display & Website
    is_featured = fields.Boolean('Unggulan', help="Tampilkan di halaman utama")
    website_published = fields.Boolean('Dipublikasikan di Website', default=True)
    date = fields.Date('Tanggal Publikasi Hibah', default=fields.Date.today)
    
    # SEO Fields
    slug = fields.Char('URL Slug', help="Slug untuk URL (otomatis dari nama jika kosong)")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci SEO, pisahkan dengan koma")
    
    # Computed Fields
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration_months = round(delta.days / 30)
            else:
                record.duration_months = 0
    
    @api.depends('total_amount', 'disbursed_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.total_amount - record.disbursed_amount
    
    @api.depends('budget_line_ids.amount')
    def _compute_budget_total(self):
        for record in self:
            record.budget_total = sum(record.budget_line_ids.mapped('amount'))
    
    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug(vals['name'])
            if not vals.get('meta_title') and vals.get('name'):
                vals['meta_title'] = vals['name']
        
        return super(HibahPendanaanPost, self).create(vals_list)
    
    def write(self, vals):
        if 'name' in vals and not vals.get('slug'):
            vals['slug'] = self._generate_slug(vals['name'])
        if 'name' in vals and not vals.get('meta_title'):
            vals['meta_title'] = vals['name']
        return super(HibahPendanaanPost, self).write(vals)
    
    def _generate_slug(self, name):
        """Generate URL-friendly slug from name"""
        import re
        if not name:
            return ''
        # Convert to lowercase and replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def toggle_website_published(self):
        """Toggle website published status"""
        for record in self:
            record.website_published = not record.website_published
        return True
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise UserError("Tanggal mulai tidak boleh lebih besar dari tanggal selesai.")
    
    @api.constrains('total_amount', 'disbursed_amount')
    def _check_amounts(self):
        for record in self:
            if record.total_amount < 0:
                raise UserError("Total anggaran tidak boleh negatif.")
            if record.disbursed_amount < 0:
                raise UserError("Dana dicairkan tidak boleh negatif.")
            if record.disbursed_amount > record.total_amount:
                raise UserError("Dana dicairkan tidak boleh lebih besar dari total anggaran.")
