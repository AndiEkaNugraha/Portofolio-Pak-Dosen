# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def _get_classified_fields(self, fields=None):
        """Override to allow many2many fields in config settings"""
        if fields is None:
            fields = list(self._fields.keys())
        # Use base implementation but add many2many support
        classified = super()._get_classified_fields(fields)
        if 'many2many' not in classified:
            classified['many2many'] = []
        for field in fields:
            if self._fields[field].type == 'many2many':
                classified['many2many'].append(field)
        return classified

    bimbingan_notification_email_enabled = fields.Boolean(
        string='Aktifkan Notifikasi Email',
        config_parameter='bimbingan_mahasiswa.notification_email_enabled'
    )
    
    bimbingan_notification_email = fields.Char(
        string='Email Penerima Notifikasi',
        config_parameter='bimbingan_mahasiswa.notification_email',
        help='Email dosen/admin yang akan menerima notifikasi pengajuan bimbingan'
    )
    
    # Template untuk email pengajuan baru
    bimbingan_new_subject = fields.Char(
        string='Subject Email Pengajuan Baru',
        config_parameter='bimbingan_mahasiswa.new_subject',
        default='Pengajuan Bimbingan Baru dari ${student_name}'
    )
    
    bimbingan_new_body = fields.Char(
        string='Isi Email Pengajuan Baru',
        config_parameter='bimbingan_mahasiswa.new_body',
        size=2000,
        default='Assalamualaikum, Ada pengajuan bimbingan baru dari mahasiswa ${student_name}. Detail: Jenis Bimbingan: ${guidance_type}, Tanggal: ${guidance_date}, Deskripsi: ${description}. Silakan login ke sistem untuk melihat detail lengkap.'
    )
    
    # Template untuk email perubahan status
    bimbingan_status_subject = fields.Char(
        string='Subject Email Perubahan Status',
        config_parameter='bimbingan_mahasiswa.status_subject',
        default='Status Bimbingan: ${status}'
    )
    
    bimbingan_status_body = fields.Char(
        string='Isi Email Perubahan Status',
        config_parameter='bimbingan_mahasiswa.status_body',
        size=2000,
        default='Assalamualaikum ${student_name}, Status pengajuan bimbingan Anda telah diubah menjadi: ${status}. Detail: Jenis Bimbingan: ${guidance_type}, Tanggal: ${guidance_date}. Silakan login ke portal untuk melihat detail lengkap.'
    )
    
    # Template untuk email komentar baru
    bimbingan_comment_subject = fields.Char(
        string='Subject Email Komentar Baru',
        config_parameter='bimbingan_mahasiswa.comment_subject',
        default='Komentar Baru pada Bimbingan Anda'
    )
    
    bimbingan_comment_body = fields.Char(
        string='Isi Email Komentar Baru',
        config_parameter='bimbingan_mahasiswa.comment_body',
        size=2000,
        default='Assalamualaikum ${student_name}, Ada komentar baru pada pengajuan bimbingan Anda. Detail: Jenis Bimbingan: ${guidance_type}, Tanggal: ${guidance_date}. Silakan login ke portal untuk melihat komentar lengkap.'
    )
    
    @api.model
    def default_get(self, fields):
        """Override to handle many2many fields"""
        # Handle many2many fields first
        many2many_fields = [f for f in fields if self._fields[f].type == 'many2many']
        other_fields = [f for f in fields if f not in many2many_fields]
        
        defaults = {}
        if other_fields:
            defaults = super().default_get(other_fields)
        
        # Handle many2many fields
        for field in many2many_fields:
            config_param_key = f'bimbingan_mahasiswa.{field}'
            value_str = self.env['ir.config_parameter'].sudo().get_param(config_param_key, default='')
            if value_str:
                try:
                    ids = [int(id_str) for id_str in value_str.split(',') if id_str.strip()]
                    defaults[field] = [(6, 0, ids)]  # Replace with new ids
                except ValueError:
                    defaults[field] = [(6, 0, [])]
            else:
                defaults[field] = [(6, 0, [])]
        
        return defaults

    def set_values(self):
        """Override to handle many2many fields"""
        # Handle many2many fields first
        for field_name in self._fields:
            field = self._fields[field_name]
            if field.type == 'many2many' and field_name.startswith('bimbingan_website'):
                value = getattr(self, field_name)
                config_param_key = f'bimbingan_mahasiswa.{field_name}'
                if value:
                    ids_str = ','.join(str(id) for id in value.ids)
                else:
                    ids_str = ''
                self.env['ir.config_parameter'].sudo().set_param(config_param_key, ids_str)
        
        # Call super for other fields
        super().set_values()

    def execute(self):
        """Override to handle many2many fields in execute"""
        # Handle many2many fields before calling super
        for field in self._get_classified_fields()['many2many']:
            value = getattr(self, field)
            config_param_key = f'bimbingan_mahasiswa.{field}'
            if value:
                ids_str = ','.join(str(id) for id in value.ids)
            else:
                ids_str = ''
            self.env['ir.config_parameter'].sudo().set_param(config_param_key, ids_str)
        
        # Call super execute
        return super().execute()


    bimbingan_website_ids = fields.Many2many('website', string='Website yang Menggunakan Modul Bimbingan', 
                                             help='Pilih website mana saja yang akan menampilkan fitur bimbingan mahasiswa. Jika kosong, akan muncul di semua website.')

    bimbingan_notification_email_enabled = fields.Boolean(
        string='Aktifkan Notifikasi Email',
        config_parameter='bimbingan_mahasiswa.notification_email_enabled'
    )
