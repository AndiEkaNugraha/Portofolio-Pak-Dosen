# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ProyekPenelitianPost(models.Model):
    _name = 'proyek.penelitian.post'
    _description = 'Proyek Penelitian'
    _order = 'start_date desc, id desc'

    # Basic Information
    name = fields.Char('Judul Proyek', required=True)
    subtitle = fields.Char('Subjudul/Tagline', help="Tagline atau deskripsi singkat proyek")
    blog_id = fields.Many2one('proyek.penelitian.blog', 'Kategori', required=True, ondelete='cascade')
    
    # Project Details
    project_code = fields.Char('Kode Proyek', help="Nomor/kode unik proyek")
    principal_investigator = fields.Char('Ketua Peneliti', required=True)
    co_investigators = fields.Text('Anggota Peneliti', help="Nama anggota peneliti, pisahkan dengan baris baru")
    
    # Timeline & Status
    start_date = fields.Date('Tanggal Mulai', required=True)
    end_date = fields.Date('Tanggal Selesai')
    duration_months = fields.Integer('Durasi (Bulan)', compute='_compute_duration', store=True)
    status = fields.Selection([
        ('proposal', 'Tahap Proposal'),
        ('active', 'Sedang Berjalan'),
        ('completed', 'Selesai'),
        ('suspended', 'Ditunda'),
        ('cancelled', 'Dibatalkan')
    ], string='Status Proyek', required=True, default='proposal')
    
    progress_percentage = fields.Float('Progress (%)', help="Persentase penyelesaian proyek (0-100)")
    
    # Funding Information
    funding_source = fields.Char('Sumber Pendanaan', required=True, help="Contoh: Kemendikbud, BRIN, Industri")
    funding_source_url = fields.Char('URL Sumber Pendanaan', help="URL website pemberi dana")
    funding_scheme = fields.Char('Skema Pendanaan', help="Contoh: Hibah Penelitian Dasar, PKM, dll")
    total_budget = fields.Float('Total Anggaran (Rp)')
    budget_year = fields.Char('Tahun Anggaran', help="Contoh: 2024, 2023-2025")
    
    # Research Information
    research_area = fields.Char('Bidang Penelitian', help="Area/bidang ilmu penelitian")
    keywords = fields.Char('Kata Kunci', help="Kata kunci penelitian, pisahkan dengan koma")
    research_objectives = fields.Html('Tujuan Penelitian', help="Tujuan dan target yang ingin dicapai")
    methodology = fields.Html('Metodologi', help="Metode penelitian yang digunakan")
    expected_outcomes = fields.Html('Luaran yang Diharapkan', help="Output dan outcome yang diharapkan")
    
    # Collaboration & Partnership  
    partner_institutions = fields.Text('Institusi Mitra', help="Institusi yang berkolaborasi, pisahkan dengan baris baru")
    industry_partners = fields.Text('Mitra Industri', help="Perusahaan atau industri yang terlibat")
    international_collaboration = fields.Boolean('Kolaborasi Internasional')
    international_partners = fields.Text('Mitra Internasional', help="Institusi luar negeri yang berkolaborasi")
    
    # Students & Team
    phd_students = fields.Text('Mahasiswa S3 Terlibat', help="Mahasiswa doktoral yang terlibat dalam proyek")
    master_students = fields.Text('Mahasiswa S2 Terlibat', help="Mahasiswa magister yang terlibat")
    undergrad_students = fields.Text('Mahasiswa S1 Terlibat', help="Mahasiswa sarjana yang terlibat")
    research_assistants = fields.Text('Asisten Peneliti', help="Tenaga peneliti dan asisten yang terlibat")
    
    # Outputs & Publications
    publications = fields.Html('Publikasi yang Dihasilkan', help="Jurnal, konferensi, dan publikasi lainnya")
    patents_ip = fields.Text('Paten/HKI', help="Paten atau HKI yang dihasilkan dari proyek")
    prototypes = fields.Html('Prototipe/Produk', help="Prototipe atau produk yang dikembangkan")
    conference_presentations = fields.Html('Presentasi Konferensi', help="Presentasi di konferensi atau seminar")
    
    # Related Products - NEW FIELD
    product_ids = fields.One2many('proyek.penelitian.produk', 'proyek_id', string='Produk Penelitian', help="Produk penelitian yang terkait dengan proyek ini")
    
    # Impact & Achievement
    achievements = fields.Html('Pencapaian & Prestasi', help="Penghargaan atau pencapaian dari proyek") 
    social_impact = fields.Html('Dampak Sosial', help="Manfaat atau dampak proyek terhadap masyarakat")
    economic_impact = fields.Html('Dampak Ekonomi', help="Dampak ekonomi atau komersialisasi hasil penelitian")
    policy_impact = fields.Html('Dampak Kebijakan', help="Pengaruh terhadap kebijakan pemerintah atau regulasi")
    
    # Media & Documentation
    project_images = fields.Binary('Foto Proyek', help="Foto kegiatan atau hasil proyek")
    project_images_filename = fields.Char('Nama File Foto')
    project_documents = fields.Binary('Dokumen Proyek', help="Proposal, laporan, atau dokumen terkait")
    project_documents_filename = fields.Char('Nama File Dokumen')
    project_video = fields.Char('Link Video', help="URL video dokumentasi atau presentasi proyek")
    
    # Content & Description
    teaser = fields.Text('Ringkasan Singkat', help="Ringkasan singkat untuk preview di website")
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap proyek untuk halaman detail")
    
    # Milestones & Progress
    milestones = fields.Html('Milestone & Target', help="Pencapaian target dan milestone proyek")
    current_activities = fields.Html('Kegiatan Saat Ini', help="Aktivitas penelitian yang sedang dilakukan")
    next_steps = fields.Html('Langkah Selanjutnya', help="Rencana kegiatan ke depan")
    
    # Contact & Links
    contact_email = fields.Char('Email Kontak')
    project_website = fields.Char('Website Proyek', help="URL website khusus proyek jika ada")
    related_links = fields.Text('Link Terkait', help="Link publikasi, media, atau sumber terkait")
    
    # Publication & Display
    date = fields.Date('Tanggal Dibuat', default=fields.Date.today, required=True)
    is_published = fields.Boolean('Dipublikasikan', default=True)
    website_published = fields.Boolean('Dipublikasikan di Website', default=True)
    is_featured = fields.Boolean('Unggulan', help="Tampilkan di halaman utama")
    
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
    
    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug(vals['name'])
            if not vals.get('meta_title') and vals.get('name'):
                vals['meta_title'] = vals['name']
        
        return super(ProyekPenelitianPost, self).create(vals_list)
    
    def write(self, vals):
        if 'name' in vals and not vals.get('slug'):
            vals['slug'] = self._generate_slug(vals['name'])
        if 'name' in vals and not vals.get('meta_title'):
            vals['meta_title'] = vals['name']
        return super(ProyekPenelitianPost, self).write(vals)
    
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
    
    @api.constrains('total_budget')
    def _check_budget(self):
        for record in self:
            if record.total_budget < 0:
                raise UserError("Anggaran tidak boleh negatif.")