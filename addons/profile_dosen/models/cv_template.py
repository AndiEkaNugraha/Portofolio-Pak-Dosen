# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CVTemplate(models.Model):
    _name = 'cv.template'
    _description = 'Template CV ATS'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Template', required=True)
    code = fields.Char('Kode Template', required=True, help="Kode unik untuk template")
    description = fields.Text('Deskripsi')
    
    # Template type
    template_type = fields.Selection([
        ('ats_standard', 'ATS Standard'),
        ('ats_modern', 'ATS Modern'),
        ('ats_professional', 'ATS Professional'),
        ('ats_academic', 'ATS Academic'),
        ('custom', 'Custom'),
    ], string='Tipe Template', default='ats_standard', required=True)
    
    # Sections to include
    include_personal_info = fields.Boolean('Informasi Pribadi', default=True)
    include_biography = fields.Boolean('Biografi', default=True)
    include_education = fields.Boolean('Pendidikan', default=True)
    include_work_experience = fields.Boolean('Pengalaman Kerja', default=True)
    include_expertise = fields.Boolean('Keahlian & Minat Riset', default=True)
    include_awards = fields.Boolean('Penghargaan', default=True)
    include_publications = fields.Boolean('Publikasi', default=True)
    include_books = fields.Boolean('Buku', default=True)
    include_patents = fields.Boolean('HKI/Paten', default=True)
    include_research_projects = fields.Boolean('Proyek Penelitian', default=True)
    include_community_service = fields.Boolean('Pengabdian Masyarakat', default=True)
    include_conferences = fields.Boolean('Konferensi/Prosiding', default=True)
    include_grants = fields.Boolean('Hibah Pendanaan', default=True)
    include_research_products = fields.Boolean('Produk Penelitian', default=True)
    include_reviewer_activities = fields.Boolean('Aktivitas Reviewer', default=True)
    include_events = fields.Boolean('Acara & Kegiatan', default=True)
    include_research_groups = fields.Boolean('Grup Riset', default=True)
    include_courses = fields.Boolean('Mata Kuliah', default=True)
    
    # Sorting options
    sort_by_year = fields.Boolean('Urutkan Berdasarkan Tahun', default=True)
    sort_descending = fields.Boolean('Urutan Terbaru Terlebih Dahulu', default=True)
    
    # Limit options
    limit_publications = fields.Integer('Limit Publikasi', default=0, help="0 = tanpa limit")
    limit_projects = fields.Integer('Limit Proyek', default=0, help="0 = tanpa limit")
    
    # Format options
    date_format = fields.Selection([
        ('full', 'DD/MM/YYYY'),
        ('month_year', 'MM/YYYY'),
        ('year_only', 'YYYY'),
    ], string='Format Tanggal', default='month_year')
    
    # Custom HTML Template (tidak perlu QWeb lagi)
    # PENTING: Gunakan Text, bukan Html, agar struktur HTML lengkap tidak di-sanitize
    custom_html_template = fields.Text('HTML Template', 
                                       help="Template HTML untuk CV. Gunakan placeholder seperti ${name}, ${education}, dll.")
    
    # CSS styling
    custom_css = fields.Text('Custom CSS', help="CSS kustom untuk styling CV")
    
    is_default = fields.Boolean('Template Default', default=False)
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Active', default=True)
    
    @api.model
    def get_default_template(self):
        """Get default CV template"""
        template = self.search([('is_default', '=', True)], limit=1)
        if not template:
            # Create default template if not exists
            template = self.create({
                'name': 'ATS Standard Template',
                'code': 'ats_standard',
                'template_type': 'ats_standard',
                'is_default': True,
            })
        return template
    
    @api.model_create_multi
    def create(self, vals_list):
        # If this is set as default, unset other defaults
        for vals in vals_list:
            if vals.get('is_default'):
                self.search([('is_default', '=', True)]).write({'is_default': False})
        return super(CVTemplate, self).create(vals_list)
    
    def write(self, vals):
        # If this is set as default, unset other defaults
        if vals.get('is_default'):
            self.search([('is_default', '=', True), ('id', 'not in', self.ids)]).write({'is_default': False})
        return super().write(vals)
