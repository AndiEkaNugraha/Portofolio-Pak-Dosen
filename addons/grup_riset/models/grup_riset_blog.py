# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class GrupRisetBlog(models.Model):
    _name = 'grup.riset.blog'
    _description = 'Kategori Grup Riset dan Laboratorium'
    _order = 'sequence, name'

    name = fields.Char('Nama Kategori', required=True, help="Contoh: Artificial Intelligence Lab, Computer Vision Research Group")
    subtitle = fields.Char('Subjudul', help="Deskripsi singkat kategori grup riset")
    description = fields.Text('Deskripsi', help="Deskripsi lengkap kategori grup riset")
    
    # Research Focus & Area
    research_area = fields.Selection([
        ('ai_ml', 'Artificial Intelligence & Machine Learning'),
        ('computer_vision', 'Computer Vision'),
        ('nlp', 'Natural Language Processing'), 
        ('robotics', 'Robotics'),
        ('iot', 'Internet of Things'),
        ('cybersecurity', 'Cybersecurity'),
        ('data_science', 'Data Science & Analytics'),
        ('software_engineering', 'Software Engineering'),
        ('network', 'Network & Communications'),
        ('hci', 'Human-Computer Interaction'),
        ('bioinformatics', 'Bioinformatics'),
        ('other', 'Lainnya')
    ], string='Area Riset Utama', required=True)
    
    lab_type = fields.Selection([
        ('research_group', 'Grup Riset'),
        ('laboratory', 'Laboratorium'),
        ('center', 'Pusat Penelitian'),
        ('unit', 'Unit Riset')
    ], string='Jenis', required=True, default='research_group')
    
    # Institution & Location
    institution = fields.Char('Institusi', help="Nama universitas atau institusi")
    faculty = fields.Char('Fakultas/Departemen')
    location = fields.Char('Lokasi', help="Lokasi fisik laboratorium/grup riset")
    
    # Statistics
    post_count = fields.Integer('Jumlah Konten', compute='_compute_post_count', store=True)
    member_count = fields.Integer('Jumlah Anggota', help="Jumlah anggota dalam grup riset")
    
    # Display & SEO
    sequence = fields.Integer('Urutan', default=10)
    is_published = fields.Boolean('Dipublikasikan', default=True)
    website_published = fields.Boolean('Dipublikasikan di Website', default=True)
    active = fields.Boolean('Aktif', default=True)
    
    # Computed fields
    display_name_full = fields.Char('Nama Lengkap', compute='_compute_display_name_full', store=True)
    
    @api.depends('name', 'subtitle')
    def _compute_display_name_full(self):
        for record in self:
            if record.subtitle:
                record.display_name_full = f"{record.name} - {record.subtitle}"
            else:
                record.display_name_full = record.name
    
    @api.depends('grup_riset_post_ids')
    def _compute_post_count(self):
        for blog in self:
            blog.post_count = len(blog.grup_riset_post_ids)
    
    # Relations
    grup_riset_post_ids = fields.One2many('grup.riset.post', 'blog_id', 'Konten Grup Riset')


class GrupRisetPost(models.Model):
    _name = 'grup.riset.post'
    _description = 'Grup Riset dan Laboratorium'
    _order = 'date desc, id desc'

    # Basic Information
    name = fields.Char('Nama Grup Riset/Lab', required=True)
    subtitle = fields.Char('Subtitle/Tagline', help="Tagline atau motto grup riset")
    blog_id = fields.Many2one('grup.riset.blog', 'Kategori', required=True, ondelete='cascade')
    
    # Leader & Team
    leader_name = fields.Char('Nama Ketua/Pembimbing', required=True)
    leader_title = fields.Char('Gelar Ketua', help="Contoh: Prof. Dr. Ir.")
    co_leaders = fields.Text('Co-Leader/Pembimbing Pendamping', help="Nama pembimbing lain, pisahkan dengan baris baru")
    
    # Team Members
    team_members = fields.Text('Anggota Tim', help="Daftar anggota tim peneliti, pisahkan dengan baris baru")
    phd_students = fields.Text('Mahasiswa S3', help="Mahasiswa doktoral yang terlibat")
    master_students = fields.Text('Mahasiswa S2', help="Mahasiswa magister yang terlibat")
    undergrad_students = fields.Text('Mahasiswa S1', help="Mahasiswa sarjana yang terlibat")
    
    # Research Information
    research_focus = fields.Text('Fokus Penelitian', required=True, help="Deskripsi fokus penelitian utama")
    research_keywords = fields.Char('Kata Kunci Penelitian', help="Keywords penelitian, pisahkan dengan koma")
    established_year = fields.Integer('Tahun Didirikan')
    
    # Facilities & Equipment
    facilities = fields.Html('Fasilitas & Peralatan', help="Deskripsi fasilitas dan peralatan yang dimiliki")
    lab_space = fields.Char('Ruang Lab', help="Contoh: Ruang B301, Lab AI Lt.3")
    equipment_list = fields.Text('Daftar Peralatan Utama', help="Daftar peralatan penting, pisahkan dengan baris baru")
    
    # Projects & Collaborations
    current_projects = fields.Html('Proyek Sedang Berjalan', help="Deskripsi proyek penelitian yang sedang aktif")
    completed_projects = fields.Html('Proyek Selesai', help="Deskripsi proyek yang telah selesai")
    collaborations = fields.Text('Kolaborasi', help="Institusi atau perusahaan yang berkolaborasi")
    
    # Publications & Achievements
    recent_publications = fields.Html('Publikasi Terbaru', help="Daftar publikasi terbaru grup riset")
    achievements = fields.Html('Pencapaian & Penghargaan', help="Pencapaian dan penghargaan yang diraih")
    patents = fields.Text('Paten/HKI', help="Paten atau HKI yang dimiliki grup")
    
    # Funding & Grants
    funding_sources = fields.Text('Sumber Pendanaan', help="Sumber pendanaan penelitian, pisahkan dengan baris baru")
    grants_received = fields.Html('Hibah yang Diterima', help="Daftar hibah penelitian yang pernah diterima")
    
    # Contact & Social
    contact_email = fields.Char('Email Kontak')
    contact_person = fields.Char('Person in Charge')
    website_url = fields.Char('Website Grup Riset', help="URL website grup riset jika ada")
    social_media = fields.Char('Media Sosial', help="Link media sosial grup riset")
    
    # Media
    group_photo = fields.Binary('Foto Grup', help="Foto anggota grup riset")
    group_photo_filename = fields.Char('Nama File Foto')
    lab_photos = fields.Binary('Foto Laboratorium', help="Foto fasilitas laboratorium")
    lab_photos_filename = fields.Char('Nama File Foto Lab')
    
    # Content & Description
    teaser = fields.Text('Ringkasan Singkat', help="Ringkasan singkat untuk preview di website")
    description = fields.Html('Deskripsi Lengkap', help="Deskripsi lengkap grup riset untuk halaman detail")
    
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
    
    # Statistics
    total_members = fields.Integer('Total Anggota', compute='_compute_total_members', store=True)
    total_students = fields.Integer('Total Mahasiswa', compute='_compute_total_students', store=True)
    
    @api.depends('team_members', 'phd_students', 'master_students', 'undergrad_students')
    def _compute_total_members(self):
        for record in self:
            total = 1  # Leader
            if record.co_leaders:
                total += len([line.strip() for line in record.co_leaders.split('\n') if line.strip()])
            if record.team_members:
                total += len([line.strip() for line in record.team_members.split('\n') if line.strip()])
            record.total_members = total
    
    @api.depends('phd_students', 'master_students', 'undergrad_students')
    def _compute_total_students(self):
        for record in self:
            total = 0
            if record.phd_students:
                total += len([line.strip() for line in record.phd_students.split('\n') if line.strip()])
            if record.master_students:
                total += len([line.strip() for line in record.master_students.split('\n') if line.strip()])
            if record.undergrad_students:
                total += len([line.strip() for line in record.undergrad_students.split('\n') if line.strip()])
            record.total_students = total
    
    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug(vals['name'])
            if not vals.get('meta_title') and vals.get('name'):
                vals['meta_title'] = vals['name']
        
        return super(GrupRisetPost, self).create(vals_list)
    
    def write(self, vals):
        if 'name' in vals and not vals.get('slug'):
            vals['slug'] = self._generate_slug(vals['name'])
        if 'name' in vals and not vals.get('meta_title'):
            vals['meta_title'] = vals['name']
        return super(GrupRisetPost, self).write(vals)
    
    def _generate_slug(self, name):
        """Generate URL-friendly slug from name"""
        import re
        if not name:
            return ''
        # Convert to lowercase and replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    @api.constrains('contact_email')
    def _check_email(self):
        import re
        for record in self:
            if record.contact_email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.contact_email):
                raise UserError("Format email tidak valid.")