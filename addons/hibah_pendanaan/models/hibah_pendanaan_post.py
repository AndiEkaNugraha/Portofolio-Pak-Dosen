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
    principal_investigator = fields.Char('Ketua/Penanggung Jawab', required=True)
    co_investigators = fields.Text('Anggota Tim', help="Nama anggota tim, pisahkan dengan baris baru")
    
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
    
    progress_percentage = fields.Float('Progress (%)', help="Persentase penyelesaian hibah (0-100)")
    
    # Funding Information
    funding_agency = fields.Char('Lembaga Pemberi Dana', required=True)
    funding_source = fields.Char('Sumber Dana', help="Detail sumber dana, contoh: APBN, APBD, Swasta")
    total_amount = fields.Float('Total Anggaran (Rp)', required=True)
    disbursed_amount = fields.Float('Dana Dicairkan (Rp)', help="Total dana yang sudah dicairkan")
    remaining_amount = fields.Float('Sisa Dana (Rp)', compute='_compute_remaining_amount', store=True)
    funding_year = fields.Char('Tahun Anggaran', help="Contoh: 2024, 2023-2025")
    
    # Budget Breakdown
    personnel_cost = fields.Float('Biaya Personel (Rp)')
    equipment_cost = fields.Float('Biaya Peralatan (Rp)')
    material_cost = fields.Float('Biaya Bahan (Rp)')
    travel_cost = fields.Float('Biaya Perjalanan (Rp)')
    other_cost = fields.Float('Biaya Lainnya (Rp)')
    overhead_percentage = fields.Float('Overhead (%)')
    
    # Research Information
    research_area = fields.Char('Bidang Penelitian', help="Area/bidang penelitian")
    keywords = fields.Char('Kata Kunci', help="Kata kunci hibah, pisahkan dengan koma")
    objectives = fields.Html('Tujuan Hibah', help="Tujuan dan target yang ingin dicapai")
    methodology = fields.Html('Metodologi', help="Metode penelitian yang digunakan")
    expected_outcomes = fields.Html('Luaran yang Diharapkan', help="Output dan outcome yang diharapkan")
    
    # Collaboration & Partnership  
    partner_institutions = fields.Text('Institusi Mitra', help="Institusi yang berkolaborasi, pisahkan dengan baris baru")
    industry_partners = fields.Text('Mitra Industri', help="Perusahaan/industri yang terlibat")
    international_collaboration = fields.Boolean('Kolaborasi Internasional')
    international_partners = fields.Text('Mitra Internasional', help="Institusi internasional yang terlibat")
    
    # Team & Human Resources
    phd_students = fields.Text('Mahasiswa S3 Terlibat', help="Nama mahasiswa S3 yang terlibat")
    master_students = fields.Text('Mahasiswa S2 Terlibat', help="Nama mahasiswa S2 yang terlibat")
    undergrad_students = fields.Text('Mahasiswa S1 Terlibat', help="Nama mahasiswa S1 yang terlibat")
    research_assistants = fields.Text('Asisten Peneliti', help="Nama asisten peneliti")
    external_experts = fields.Text('Pakar Eksternal', help="Konsultan atau pakar dari luar institusi")
    
    # Outputs & Results
    publications = fields.Html('Publikasi yang Dihasilkan', help="Daftar publikasi dari hibah ini")
    patents_ip = fields.Html('Paten/HKI', help="Paten atau hak kekayaan intelektual yang dihasilkan")
    prototypes = fields.Html('Prototipe/Produk', help="Prototipe atau produk yang dikembangkan")
    conference_presentations = fields.Text('Presentasi Konferensi', help="Konferensi/seminar yang diikuti")
    awards_recognition = fields.Html('Penghargaan', help="Penghargaan yang diterima")
    
    # Impact & Sustainability
    social_impact = fields.Html('Dampak Sosial', help="Dampak positif terhadap masyarakat")
    economic_impact = fields.Html('Dampak Ekonomi', help="Dampak ekonomi yang dihasilkan")
    environmental_impact = fields.Html('Dampak Lingkungan', help="Dampak terhadap lingkungan")
    sustainability_plan = fields.Html('Rencana Keberlanjutan', help="Rencana setelah hibah selesai")
    
    # Progress Reporting
    milestone_achieved = fields.Html('Milestone yang Dicapai', help="Pencapaian milestone utama")
    current_activities = fields.Html('Kegiatan Saat Ini', help="Aktivitas yang sedang berlangsung")
    challenges_faced = fields.Html('Tantangan yang Dihadapi', help="Masalah dan solusi")
    next_steps = fields.Html('Langkah Selanjutnya', help="Rencana ke depan")
    
    # Documentation & Reporting
    interim_reports = fields.Html('Laporan Kemajuan', help="Link atau deskripsi laporan kemajuan")
    final_report = fields.Html('Laporan Akhir', help="Link atau deskripsi laporan akhir")
    financial_reports = fields.Html('Laporan Keuangan', help="Dokumentasi penggunaan dana")
    audit_results = fields.Html('Hasil Audit', help="Hasil audit jika ada")
    
    # Content & Description
    teaser = fields.Text('Ringkasan Singkat', help="Deskripsi singkat untuk preview")
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi detail hibah/pendanaan")
    background = fields.Html('Latar Belakang', help="Latar belakang dan urgensi hibah")
    significance = fields.Html('Signifikansi', help="Pentingnya hibah ini")
    
    # Media & Documents  
    image_url = fields.Char('URL Gambar', help="Link gambar untuk ditampilkan di website")
    document_urls = fields.Text('Link Dokumen', help="Link ke dokumen terkait hibah")
    video_url = fields.Char('URL Video', help="Link video presentasi atau dokumentasi")
    
    # Contact & External Links
    contact_email = fields.Char('Email Kontak')
    contact_phone = fields.Char('Telepon Kontak')
    project_website = fields.Char('Website Proyek', help="Website khusus proyek jika ada")
    related_links = fields.Text('Link Terkait', help="Link ke artikel, berita, atau halaman terkait")
    
    # Display & Website
    is_featured = fields.Boolean('Unggulan', help="Tampilkan di halaman utama")
    website_published = fields.Boolean('Dipublikasikan di Website', default=True)
    date = fields.Date('Tanggal Publikasi', default=fields.Date.today)
    
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
    
    @api.constrains('progress_percentage')
    def _check_progress(self):
        for record in self:
            if record.progress_percentage < 0 or record.progress_percentage > 100:
                raise UserError("Progress harus antara 0-100%.")
    
    @api.constrains('total_amount', 'disbursed_amount')
    def _check_amounts(self):
        for record in self:
            if record.total_amount < 0:
                raise UserError("Total anggaran tidak boleh negatif.")
            if record.disbursed_amount < 0:
                raise UserError("Dana dicairkan tidak boleh negatif.")
            if record.disbursed_amount > record.total_amount:
                raise UserError("Dana dicairkan tidak boleh lebih besar dari total anggaran.")