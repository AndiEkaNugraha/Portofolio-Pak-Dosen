# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProyekPenelitianMitra(models.Model):
    _name = 'proyek.penelitian.mitra'
    _description = 'Mitra Kolaborasi Proyek Penelitian'
    _order = 'sequence, id'

    # Basic fields
    proyek_id = fields.Many2one('proyek.penelitian.post', 'Proyek Penelitian', required=True, ondelete='cascade')
    sequence = fields.Integer('Urutan', default=10)

    # Partner information
    name = fields.Char('Nama Mitra/Institusi', required=True, help="Nama institusi atau perusahaan mitra")
    partner_url = fields.Char('URL Website', help="URL website resmi mitra")
    partner_type = fields.Selection([
        ('academic', 'Institusi Akademik'),
        ('industry', 'Industri/Perusahaan'),
        ('government', 'Pemerintah'),
        ('ngo', 'LSM/Organisasi'),
        ('international', 'Internasional'),
        ('other', 'Lainnya')
    ], string='Tipe Mitra', required=True, default='academic')

    # Additional information
    contact_person = fields.Char('Contact Person', help="Nama orang yang dapat dihubungi")
    contact_email = fields.Char('Email Kontak', help="Email untuk komunikasi")
    role_description = fields.Text('Deskripsi Peran', help="Peran dan kontribusi mitra dalam proyek")

    # Display name
    display_name = fields.Char('Nama Tampilan', compute='_compute_display_name', store=True)

    @api.depends('name', 'partner_type')
    def _compute_display_name(self):
        for record in self:
            if record.partner_type:
                type_labels = {
                    'academic': 'Akademik',
                    'industry': 'Industri',
                    'government': 'Pemerintah',
                    'ngo': 'LSM',
                    'international': 'Internasional',
                    'other': 'Lainnya'
                }
                type_label = type_labels.get(record.partner_type, record.partner_type)
                record.display_name = f"{record.name} ({type_label})"
            else:
                record.display_name = record.name

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.display_name))
        return result