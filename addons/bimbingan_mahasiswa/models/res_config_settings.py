# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

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
