# -*- coding: utf-8 -*-
from odoo import models, fields


class MatakuliahBlog(models.Model):
    _name = 'matakuliah.blog'
    _inherit = 'blog.blog'
    _description = 'Kategori Mata Kuliah'

    # Kategori mata kuliah yang diampu dosen
    program_studi = fields.Char(string='Program Studi', size=128, required=True)
    kode_program = fields.Char(string='Kode Program', size=32)
    jenis_program = fields.Selection([
        ('regular', 'Program Reguler'),
        ('kelas_khusus', 'Kelas Khusus'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
    ], string='Jenis Program', default='regular')
    semester = fields.Char(string='Semester', size=32)
    deskripsi_program = fields.Html(string='Deskripsi Program')
