# -*- coding: utf-8 -*-

from odoo import models, fields


class BukuType(models.Model):
    _name = 'buku.type'
    _description = 'Jenis Buku'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Jenis Buku', required=True)
    code = fields.Char('Kode', required=True)
    description = fields.Text('Deskripsi')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)