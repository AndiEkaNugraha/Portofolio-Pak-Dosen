# -*- coding: utf-8 -*-

from odoo import models, fields, api

class GuidanceRequest(models.Model):
    _name = 'guidance.request'
    _description = 'Pengajuan Bimbingan Mahasiswa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    student_id = fields.Many2one('res.partner', string='Mahasiswa', required=True, 
                                 default=lambda self: self.env.user.partner_id, tracking=True)
    guidance_type = fields.Selection([
        ('akademik', 'Bimbingan Akademik'),
        ('skripsi', 'Bimbingan Skripsi'),
        ('tesis', 'Bimbingan Tesis'),
        ('disertasi', 'Bimbingan Disertasi'),
        ('lainnya', 'Bimbingan Lainnya'),
    ], string='Jenis Bimbingan', required=True, tracking=True)
    description = fields.Text('Deskripsi Pengajuan', required=True, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Lampiran')
    guidance_date = fields.Datetime('Tanggal Bimbingan', tracking=True)
    notes_ids = fields.One2many('guidance.note', 'guidance_id', string='Komentar')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Diajukan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ], string='Status', default='draft', tracking=True)
    approval_notes = fields.Text('Catatan Persetujuan/Ditolakan', tracking=True)
    submission_date = fields.Datetime('Tanggal Pengajuan', default=fields.Datetime.now)
    approval_date = fields.Datetime('Tanggal Persetujuan/Ditolakan', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('status', 'draft') == 'draft':
                vals['status'] = 'submitted'
        records = super(GuidanceRequest, self).create(vals_list)
        
        # Send email notification for new guidance request
        for record in records:
            record._send_new_guidance_notification()
        
        return records
    
    def write(self, vals):
        old_status = {rec.id: rec.status for rec in self}
        result = super(GuidanceRequest, self).write(vals)
        
        # Send notification if status changed
        if 'status' in vals:
            for record in self:
                if old_status[record.id] != record.status:
                    record._send_status_change_notification()
        
        return result

    def _send_new_guidance_notification(self):
        """Send email notification when new guidance request is created"""
        self.ensure_one()
        
        # Get config parameters
        config_param = self.env['ir.config_parameter'].sudo()
        enabled = config_param.get_param('bimbingan_mahasiswa.notification_email_enabled', default=False)
        notification_email = config_param.get_param('bimbingan_mahasiswa.notification_email')
        
        if not enabled or not notification_email:
            return
        
        # Get email templates
        subject_template = config_param.get_param('bimbingan_mahasiswa.new_subject', 
                                                   default='Pengajuan Bimbingan Baru dari ${student_name}')
        body_template = config_param.get_param('bimbingan_mahasiswa.new_body', 
                                               default='Ada pengajuan bimbingan baru dari ${student_name}')
        
        # Prepare variables for template
        type_map = {
            'akademik': 'Bimbingan Akademik',
            'skripsi': 'Bimbingan Skripsi',
            'tesis': 'Bimbingan Tesis',
            'disertasi': 'Bimbingan Disertasi',
            'lainnya': 'Bimbingan Lainnya',
        }
        
        status_map = {
            'draft': 'Draft',
            'submitted': 'Diajukan',
            'approved': 'Disetujui',
            'rejected': 'Ditolak',
        }
        
        variables = {
            'student_name': self.student_id.name,
            'guidance_type': type_map.get(self.guidance_type, self.guidance_type),
            'guidance_date': self.guidance_date.strftime('%d/%m/%Y %H:%M') if self.guidance_date else '-',
            'description': self.description,
            'status': status_map.get(self.status, self.status),
        }
        
        # Replace variables in template
        subject = subject_template
        body = body_template
        for key, value in variables.items():
            subject = subject.replace(f'${{{key}}}', str(value))
            body = body.replace(f'${{{key}}}', str(value))
        
        # Send email directly using mail.mail
        mail_values = {
            'subject': subject,
            'body_html': f'<pre>{body}</pre>',
            'email_to': notification_email,
            'email_from': self.env.user.email or self.env.company.email,
            'auto_delete': True,
        }
        self.env['mail.mail'].sudo().create(mail_values).send()
    
    def _send_status_change_notification(self):
        """Send email notification when status changes"""
        self.ensure_one()
        
        # Get config parameters
        config_param = self.env['ir.config_parameter'].sudo()
        enabled = config_param.get_param('bimbingan_mahasiswa.notification_email_enabled', default=False)
        notification_email = config_param.get_param('bimbingan_mahasiswa.notification_email')
        
        if not enabled:
            return
        
        # Get email templates
        subject_template = config_param.get_param('bimbingan_mahasiswa.status_subject', 
                                                   default='Status Bimbingan: ${status}')
        body_template = config_param.get_param('bimbingan_mahasiswa.status_body', 
                                               default='Status pengajuan bimbingan telah diubah menjadi: ${status}')
        
        # Prepare variables for template
        type_map = {
            'akademik': 'Bimbingan Akademik',
            'skripsi': 'Bimbingan Skripsi',
            'tesis': 'Bimbingan Tesis',
            'disertasi': 'Bimbingan Disertasi',
            'lainnya': 'Bimbingan Lainnya',
        }
        
        status_map = {
            'draft': 'Draft',
            'submitted': 'Diajukan',
            'approved': 'Disetujui',
            'rejected': 'Ditolak',
        }
        
        variables = {
            'student_name': self.student_id.name,
            'guidance_type': type_map.get(self.guidance_type, self.guidance_type),
            'guidance_date': self.guidance_date.strftime('%d/%m/%Y %H:%M') if self.guidance_date else '-',
            'description': self.description,
            'status': status_map.get(self.status, self.status),
        }
        
        # Replace variables in template
        subject = subject_template
        body = body_template
        for key, value in variables.items():
            subject = subject.replace(f'${{{key}}}', str(value))
            body = body.replace(f'${{{key}}}', str(value))
        
        # Send to both student and config email
        recipients = []
        if self.student_id.email:
            recipients.append(self.student_id.email)
        if notification_email:
            recipients.append(notification_email)
        
        if recipients:
            mail_values = {
                'subject': subject,
                'body_html': f'<pre>{body}</pre>',
                'email_to': ','.join(recipients),
                'email_from': self.env.company.email,
                'auto_delete': True,
            }
            self.env['mail.mail'].sudo().create(mail_values).send()

    def action_approve(self):
        self.write({
            'status': 'approved',
            'approval_date': fields.Datetime.now(),
        })

    def action_reject(self):
        self.write({
            'status': 'rejected',
            'approval_date': fields.Datetime.now(),
        })


class GuidanceNote(models.Model):
    _name = 'guidance.note'
    _description = 'Komentar Bimbingan'
    _order = 'create_date desc'

    guidance_id = fields.Many2one('guidance.request', string='Pengajuan Bimbingan', required=True, ondelete='cascade')
    note = fields.Html('Komentar', required=True)
    create_date = fields.Datetime('Tanggal', default=fields.Datetime.now, readonly=True)
    create_uid = fields.Many2one('res.users', string='Dibuat Oleh', default=lambda self: self.env.user, readonly=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super(GuidanceNote, self).create(vals_list)
        
        # Send email notification for new comment
        for record in records:
            record._send_new_comment_notification()
        
        return records
    
    def _send_new_comment_notification(self):
        """Send email notification when new comment is added"""
        self.ensure_one()
        
        if not self.guidance_id:
            return
        
        guidance = self.guidance_id
        
        # Get config parameters
        config_param = self.env['ir.config_parameter'].sudo()
        enabled = config_param.get_param('bimbingan_mahasiswa.notification_email_enabled', default=False)
        notification_email = config_param.get_param('bimbingan_mahasiswa.notification_email')
        
        if not enabled:
            return
        
        # Get email templates
        subject_template = config_param.get_param('bimbingan_mahasiswa.comment_subject', 
                                                   default='Komentar Baru pada Bimbingan Anda')
        body_template = config_param.get_param('bimbingan_mahasiswa.comment_body', 
                                               default='Ada komentar baru pada pengajuan bimbingan Anda.')
        
        # Prepare variables for template
        type_map = {
            'akademik': 'Bimbingan Akademik',
            'skripsi': 'Bimbingan Skripsi',
            'tesis': 'Bimbingan Tesis',
            'disertasi': 'Bimbingan Disertasi',
            'lainnya': 'Bimbingan Lainnya',
        }
        
        status_map = {
            'draft': 'Draft',
            'submitted': 'Diajukan',
            'approved': 'Disetujui',
            'rejected': 'Ditolak',
        }
        
        variables = {
            'student_name': guidance.student_id.name,
            'guidance_type': type_map.get(guidance.guidance_type, guidance.guidance_type),
            'guidance_date': guidance.guidance_date.strftime('%d/%m/%Y %H:%M') if guidance.guidance_date else '-',
            'description': guidance.description,
            'status': status_map.get(guidance.status, guidance.status),
        }
        
        # Replace variables in template
        subject = subject_template
        body = body_template
        for key, value in variables.items():
            subject = subject.replace(f'${{{key}}}', str(value))
            body = body.replace(f'${{{key}}}', str(value))
        
        # Send to both student and config email
        recipients = []
        if guidance.student_id.email and self.create_uid.id != guidance.student_id.user_ids[0].id if guidance.student_id.user_ids else True:
            recipients.append(guidance.student_id.email)
        if notification_email:
            recipients.append(notification_email)
        
        if recipients:
            mail_values = {
                'subject': subject,
                'body_html': f'<pre>{body}</pre>',
                'email_to': ','.join(recipients),
                'email_from': self.env.company.email,
                'auto_delete': True,
            }
            self.env['mail.mail'].sudo().create(mail_values).send()