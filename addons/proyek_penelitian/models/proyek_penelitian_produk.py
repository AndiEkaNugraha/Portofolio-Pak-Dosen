# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProyekPenelitianProduk(models.Model):
    _name = 'proyek.penelitian.produk'
    _description = 'Produk Terkait Proyek Penelitian'
    _order = 'id'

    # Basic fields
    proyek_id = fields.Many2one('proyek.penelitian.post', 'Proyek Penelitian', required=True, ondelete='cascade')
    # sequence = fields.Integer('Urutan', default=10)  # REMOVED - not used in website

    # Product reference - menggunakan reference field untuk berbagai model
    product_ref = fields.Reference([
        ('buku.post', 'Buku'),
        ('jurnal.post', 'Jurnal Ilmiah'),
        ('produk.post', 'Produk Penelitian'),
        ('hki.post', 'HKI/Paten'),
        ('prosiding.post', 'Prosiding Konferensi')
    ], string='Produk', required=True)

    # Computed fields untuk display
    product_name = fields.Char('Nama Produk', compute='_compute_product_info', store=True)
    product_type = fields.Char('Jenis Produk', compute='_compute_product_info', store=True)
    product_year = fields.Integer('Tahun', compute='_compute_product_info', store=True)
    product_url = fields.Char('URL Produk', compute='_compute_product_info', store=True)

    @api.depends('product_ref')
    def _compute_product_info(self):
        for record in self:
            if record.product_ref:
                # product_ref is already the referenced record object
                ref_record = record.product_ref
                ref_model = ref_record._name
                ref_id = ref_record.id

                if ref_record.exists():
                    record.product_name = ref_record.name

                    # Set product type based on model
                    type_mapping = {
                        'buku.post': 'Buku',
                        'jurnal.post': 'Jurnal Ilmiah',
                        'produk.post': 'Produk Penelitian',
                        'hki.post': 'HKI/Paten',
                        'prosiding.post': 'Prosiding Konferensi'
                    }
                    record.product_type = type_mapping.get(ref_model, 'Produk')

                    # Set year based on model
                    if ref_model == 'buku.post':
                        record.product_year = ref_record.publication_year
                        if ref_record.slug:
                            record.product_url = f"/buku/detail/{ref_record.slug}"
                        else:
                            record.product_url = f"/buku/detail/{ref_id}"
                    elif ref_model == 'jurnal.post':
                        record.product_year = ref_record.publication_year
                        if ref_record.slug:
                            record.product_url = f"/jurnal/artikel/{ref_record.slug}-{ref_id}"
                        else:
                            record.product_url = f"/jurnal/artikel/{ref_id}"
                    elif ref_model == 'produk.post':
                        record.product_year = ref_record.development_date.year if ref_record.development_date else False
                        if ref_record.slug:
                            record.product_url = f"/produk/detail/{ref_record.slug}"
                        else:
                            record.product_url = f"/produk/detail/{ref_id}"
                    elif ref_model == 'hki.post':
                        record.product_year = ref_record.application_year
                        if ref_record.slug:
                            record.product_url = f"/hki/detail/{ref_record.slug}-{ref_id}"
                        else:
                            record.product_url = f"/hki/detail/{ref_id}"
                    elif ref_model == 'prosiding.post':
                        record.product_year = ref_record.conference_year
                        if ref_record.slug:
                            record.product_url = f"/prosiding/paper/{ref_record.slug}"
                        else:
                            record.product_url = f"/prosiding/paper/{ref_id}"
                    else:
                        record.product_year = False
                        record.product_url = False
                else:
                    record.product_name = False
                    record.product_type = False
                    record.product_year = False
                    record.product_url = False
            else:
                record.product_name = False
                record.product_type = False
                record.product_year = False
                record.product_url = False

    def name_get(self):
        result = []
        for record in self:
            name = record.product_name or 'Produk'
            if record.product_type:
                name = f"{record.product_type}: {name}"
            result.append((record.id, name))
        return result