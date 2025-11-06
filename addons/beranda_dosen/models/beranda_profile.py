# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import re


class BerandaProfile(models.Model):
    _name = 'beranda.profile'
    _description = 'Profil Dosen untuk Beranda'
    _order = 'sequence, id desc'

    # Basic Information
    name = fields.Char('Nama Lengkap', required=True)
    title = fields.Char('Gelar Akademik', help="Contoh: Prof. Dr. Ir., M.Kom.")
    position = fields.Char('Jabatan', required=True, help="Contoh: Profesor, Dosen Senior, Head of Department")
    institution = fields.Char('Institusi', required=True, help="Nama universitas atau institusi")
    department = fields.Char('Departemen/Fakultas', help="Contoh: Fakultas Teknik Informatika")
    
    # Contact Information
    email = fields.Char('Email Profesional', required=True)
    phone = fields.Char('Telepon')
    office_address = fields.Text('Alamat Kantor')
    website_url = fields.Char('Website Personal', help="URL website personal")
    
    # Professional Photo
    profile_photo = fields.Binary('Foto Profil Profesional', required=True, help="Upload foto profesional untuk beranda")
    profile_photo_filename = fields.Char('Nama File Foto')
    
    # About Me
    short_bio = fields.Text('Bio Singkat', required=True, help="Bio singkat untuk hero section (max 200 karakter)")
    about_me = fields.Html('Tentang Saya', help="Deskripsi lengkap tentang latar belakang dan keahlian")
    vision_mission = fields.Html('Visi & Misi', help="Visi dan misi dalam bidang akademik dan penelitian")
    
    # Professional Background
    education_background = fields.Html('Latar Belakang Pendidikan')
    work_experience = fields.Html('Pengalaman Kerja')
    expertise_areas = fields.Text('Bidang Keahlian', help="Daftar bidang keahlian, pisahkan dengan koma")
    
    # Research & Academic Stats
    total_publications = fields.Integer('Total Publikasi', help="Jumlah total publikasi ilmiah")
    total_research_projects = fields.Integer('Total Proyek Penelitian')
    total_patents = fields.Integer('Total Paten/HKI')
    years_experience = fields.Integer('Tahun Pengalaman', help="Pengalaman dalam bidang akademik")
    h_index = fields.Integer('H-Index', help="H-Index dari Google Scholar atau Scopus")
    total_citations = fields.Integer('Total Sitasi')
    
    # Social Media & Links
    linkedin_url = fields.Char('LinkedIn')
    twitter_url = fields.Char('Twitter/X')
    google_scholar_url = fields.Char('Google Scholar')
    researchgate_url = fields.Char('ResearchGate')
    orcid_url = fields.Char('ORCID')
    scopus_url = fields.Char('Scopus')
    
    # CV & Documents
    cv_file = fields.Binary('File CV', help="Upload file CV dalam format PDF")
    cv_filename = fields.Char('Nama File CV')
    cv_last_updated = fields.Date('CV Terakhir Diperbarui', default=fields.Date.today)
    
    # CTA Settings
    show_research_cta = fields.Boolean('Tampilkan "Lihat Riset Saya"', default=True)
    show_cv_download = fields.Boolean('Tampilkan "Download CV"', default=True)
    show_collaboration_cta = fields.Boolean('Tampilkan "Hubungi untuk Kolaborasi"', default=True)
    show_publication_cta = fields.Boolean('Tampilkan "Lihat Publikasi"', default=True)
    
    research_cta_url = fields.Char('URL Riset', default='/penelitian', help="URL untuk button Lihat Riset")
    collaboration_email = fields.Char('Email Kolaborasi', help="Email khusus untuk kolaborasi (default: email profesional)")
    
    # Display Settings
    is_active = fields.Boolean('Aktif di Beranda', default=True, help="Tampilkan profil ini di beranda")
    sequence = fields.Integer('Urutan', default=10, help="Urutan tampilan jika ada multiple profile")
    theme_color = fields.Selection([
        ('blue', 'Biru'),
        ('green', 'Hijau'),
        ('red', 'Merah'),
        ('purple', 'Ungu'),
        ('orange', 'Orange'),
        ('dark', 'Gelap'),
    ], string='Tema Warna', default='blue', help="Tema warna untuk beranda")
    
    # SEO
    slug = fields.Char('URL Slug', help="Slug untuk URL beranda (otomatis dari nama jika kosong)")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan nama jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci SEO, pisahkan dengan koma")
    
    # Computed fields
    display_name_with_title = fields.Char('Nama dengan Gelar', compute='_compute_display_name_with_title', store=True)
    total_achievements = fields.Integer('Total Pencapaian', compute='_compute_total_achievements')
    expertise_list = fields.Char('Daftar Keahlian', compute='_compute_expertise_list', store=True)
    
    @api.depends('name', 'title')
    def _compute_display_name_with_title(self):
        for record in self:
            if record.title:
                record.display_name_with_title = f"{record.title} {record.name}"
            else:
                record.display_name_with_title = record.name
    
    @api.depends('total_publications', 'total_research_projects', 'total_patents')
    def _compute_total_achievements(self):
        for record in self:
            record.total_achievements = (record.total_publications or 0) + \
                                      (record.total_research_projects or 0) + \
                                      (record.total_patents or 0)
    
    @api.depends('expertise_areas')
    def _compute_expertise_list(self):
        for record in self:
            if record.expertise_areas:
                # Convert comma-separated string to formatted list
                areas = [area.strip() for area in record.expertise_areas.split(',') if area.strip()]
                record.expertise_list = ', '.join(areas[:5])  # Limit to first 5 for display
            else:
                record.expertise_list = ''
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.email):
                raise UserError("Format email tidak valid.")
    
    @api.constrains('short_bio')
    def _check_short_bio_length(self):
        for record in self:
            if record.short_bio and len(record.short_bio) > 200:
                raise UserError("Bio singkat tidak boleh lebih dari 200 karakter.")
    
    def create(self, vals):
        # Handle both single dict and list of dicts (vals_list from @api.model behavior)
        if isinstance(vals, list):
            for val in vals:
                if not val.get('slug') and val.get('name'):
                    val['slug'] = self._generate_slug(val['name'])
        else:
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug(vals['name'])
        return super(BerandaProfile, self).create(vals)
    
    def write(self, vals):
        if 'name' in vals and not vals.get('slug'):
            vals['slug'] = self._generate_slug(vals['name'])
        return super(BerandaProfile, self).write(vals)
    
    def _generate_slug(self, name):
        """Generate URL-friendly slug from name"""
        import re
        if not name:
            return ''
        # Convert to lowercase and replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def action_preview_homepage(self):
        """Action to preview homepage"""
        return {
            'type': 'ir.actions.act_url',
            'url': '/',
            'target': 'new',
        }
    
    def action_download_cv(self):
        """Action to download CV"""
        if not self.cv_file:
            raise UserError("File CV belum diupload.")
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/beranda.profile/{self.id}/cv_file/{self.cv_filename or "CV.pdf"}',
            'target': 'new',
        }


class BerandaAchievement(models.Model):
    _name = 'beranda.achievement'
    _description = 'Pencapaian untuk Highlight di Beranda'
    _order = 'date desc, sequence, id desc'
    
    name = fields.Char('Judul Pencapaian', required=True)
    description = fields.Text('Deskripsi')
    date = fields.Date('Tanggal', required=True)
    category = fields.Selection([
        ('award', 'Penghargaan'),
        ('publication', 'Publikasi'),
        ('research', 'Penelitian'),
        ('patent', 'Paten/HKI'),
        ('conference', 'Konferensi'),
        ('collaboration', 'Kolaborasi'),
        ('grant', 'Hibah Penelitian'),
        ('other', 'Lainnya'),
    ], string='Kategori', required=True, default='award')
    
    profile_id = fields.Many2one('beranda.profile', 'Profil', required=True, ondelete='cascade')
    
    # Display settings
    is_highlight = fields.Boolean('Tampilkan di Highlight', default=True, help="Tampilkan pencapaian ini di section highlight beranda")
    sequence = fields.Integer('Urutan', default=10)
    
    # Links and media
    url = fields.Char('Link Terkait', help="URL untuk informasi lebih lanjut")
    image = fields.Binary('Gambar/Sertifikat')
    image_filename = fields.Char('Nama File Gambar')
    
    # Computed
    category_icon = fields.Char('Icon Kategori', compute='_compute_category_icon')
    
    @api.depends('category')
    def _compute_category_icon(self):
        icon_map = {
            'award': 'fa-trophy',
            'publication': 'fa-book',
            'research': 'fa-flask',
            'patent': 'fa-lightbulb-o',
            'conference': 'fa-users',
            'collaboration': 'fa-handshake-o',
            'grant': 'fa-money',
            'other': 'fa-star',
        }
        for record in self:
            record.category_icon = icon_map.get(record.category, 'fa-star')