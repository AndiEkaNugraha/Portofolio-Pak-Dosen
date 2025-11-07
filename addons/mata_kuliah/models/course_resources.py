# -*- coding: utf-8 -*-

from odoo import models, fields


class CourseTextbook(models.Model):
    _name = 'course.textbook'
    _description = 'Buku Referensi Mata Kuliah'
    _order = 'sequence, name'

    name = fields.Char('Judul Buku', required=True)
    author = fields.Char('Penulis')
    publisher = fields.Char('Penerbit')
    year = fields.Integer('Tahun Terbit')
    isbn = fields.Char('ISBN/ISSN')
    sequence = fields.Integer('Urutan', default=10)

    # Relasi ke mata kuliah
    course_id = fields.Many2one('mata_kuliah.post', string='Mata Kuliah', ondelete='cascade')


class CourseResource(models.Model):
    _name = 'course.resource'
    _description = 'Sumber Belajar Tambahan Mata Kuliah'
    _order = 'sequence, name'

    name = fields.Char('Nama Sumber', required=True)
    resource_type = fields.Selection([
        ('website', 'Website'),
        ('video', 'Video'),
        ('document', 'Dokumen'),
        ('software', 'Software'),
        ('other', 'Lainnya')
    ], string='Tipe Sumber', default='website')
    url = fields.Char('URL/Link')
    description = fields.Text('Deskripsi')
    sequence = fields.Integer('Urutan', default=10)

    # Relasi ke mata kuliah
    course_id = fields.Many2one('mata_kuliah.post', string='Mata Kuliah', ondelete='cascade')