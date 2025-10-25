# -*- coding: utf-8 -*-

from odoo import models, fields


class Publisher(models.Model):
    _name = 'book.publisher'
    _description = 'Penerbit'
    _order = 'name'
    
    name = fields.Char('Nama Penerbit', required=True)
    code = fields.Char('Kode')
    country = fields.Char('Negara')
    city = fields.Char('Kota')
    website = fields.Char('Website')
    email = fields.Char('Email')
    phone = fields.Char('Telepon')
    description = fields.Text('Deskripsi')
    active = fields.Boolean('Aktif', default=True)