# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = 'Tahun Akademik'
    _order = 'name desc'
    
    name = fields.Char('Tahun Akademik', required=True, help="Format: 2023/2024")
    start_year = fields.Integer('Tahun Mulai', required=True)
    end_year = fields.Integer('Tahun Akhir', required=True)
    is_active = fields.Boolean('Aktif', default=True)
    
    # Computed field for course count
    course_count = fields.Integer('Jumlah Mata Kuliah', compute='_compute_course_count', store=True)
    
    # Computed field for semester stats
    semester_stats = fields.Json('Statistik Semester', compute='_compute_semester_stats')
    
    # Relasi ke mata kuliah
    course_ids = fields.Many2many('mata_kuliah.post', 'course_academic_year_rel', 'academic_year_id', 'course_id', string='Mata Kuliah')
    
    @api.depends('course_ids')
    def _compute_course_count(self):
        for year in self:
            year.course_count = len(year.course_ids)
    
    @api.depends('course_ids.semester')
    def _compute_semester_stats(self):
        """Compute semester statistics for this academic year"""
        for year in self:
            year.semester_stats = year.get_course_count_by_semester()
    
    @api.model
    def create(self, vals_list):
        """Auto-generate name if not provided"""
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            if not vals.get('name') and vals.get('start_year') and vals.get('end_year'):
                vals['name'] = f"{vals['start_year']}/{vals['end_year']}"
        
        return super(AcademicYear, self).create(vals_list)
    
    @api.onchange('start_year', 'end_year')
    def _onchange_years(self):
        """Auto-generate name when years change"""
        if self.start_year and self.end_year:
            self.name = f"{self.start_year}/{self.end_year}"
        elif self.start_year:
            self.name = f"{self.start_year}/{(self.start_year + 1) % 100}"
    
    @api.constrains('start_year', 'end_year')
    def _check_years(self):
        """Validate that end_year is start_year + 1"""
        for record in self:
            if record.start_year and record.end_year:
                if record.end_year != record.start_year + 1:
                    raise ValueError("Tahun akhir harus tahun mulai + 1")
    
    def get_course_count_by_semester(self):
        """Return course count grouped by semester"""
        self.ensure_one()
        semesters = ['1', '2', '3', '4', '5', '6', '7', '8', 'odd', 'even', 'both']
        result = {}
        
        for semester in semesters:
            count = len(self.course_ids.filtered(lambda c: c.semester == semester))
            if count > 0:
                result[semester] = count
        
        return result