# -*- coding: utf-8 -*-

from odoo import models, fields


class AcaraType(models.Model):
    _name = 'acara.type'
    _description = 'Tipe Acara Dosen'
    _order = 'sequence, name'

    name = fields.Char(string='Nama Tipe', required=True)
    code = fields.Char(string='Kode', required=True)
    description = fields.Text(string='Deskripsi')
    sequence = fields.Integer(string='Urutan', default=10)
    active = fields.Boolean(string='Aktif', default=True, help="Set to false to hide this type without deleting it")
    color = fields.Integer(string='Color Index', help="Color for display in kanban view")

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Kode tipe acara harus unik!'),
    ]