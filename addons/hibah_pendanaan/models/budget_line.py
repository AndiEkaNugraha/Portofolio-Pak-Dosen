# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HibahBudgetLine(models.Model):
    _name = 'hibah.budget.line'
    _description = 'Rincian Anggaran Hibah'
    _order = 'sequence, id'

    hibah_id = fields.Many2one('hibah.pendanaan.post', 'Hibah', required=True, ondelete='cascade')
    sequence = fields.Integer('Urutan', default=10)
    
    category = fields.Char('Kategori Biaya', required=True, help="Contoh: Personel, Peralatan, Bahan, Perjalanan, dll")
    description = fields.Text('Deskripsi', help="Detail dari item biaya ini")
    amount = fields.Float('Jumlah (Rp)', required=True)
    notes = fields.Char('Catatan')
    
    # Currency for monetary widget
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                   default=lambda self: self.env.company.currency_id)
    
    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                from odoo.exceptions import UserError
                raise UserError("Jumlah biaya tidak boleh negatif.")
