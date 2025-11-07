# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import base64
import datetime


class BimbinganPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        values['guidance_count'] = request.env['guidance.request'].search_count([
            ('student_id', '=', partner.id)
        ])
        return values

    @http.route(['/my/guidance', '/my/guidance/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_guidance(self, page=1, **kw):
        partner = request.env.user.partner_id
        domain = [('student_id', '=', partner.id)]
        guidance_requests = request.env['guidance.request'].search(domain, order='submission_date desc')
        guidance_count = len(guidance_requests)
        pager = request.website.pager(url='/my/guidance', total=guidance_count, page=page, step=10)
        guidance_requests = guidance_requests[pager['offset']:pager['offset'] + 10]
        values = {
            'guidance_requests': guidance_requests,
            'guidance_count': guidance_count,
            'pager': pager,
            'page_name': 'my_guidance',
            'default_url': '/my/guidance',
        }
        return request.render('bimbingan_mahasiswa.portal_my_guidance', values)

    @http.route('/my/guidance/<int:guidance_id>', type='http', auth="user", website=True)
    def portal_guidance_detail(self, guidance_id, **kw):
        partner = request.env.user.partner_id
        guidance = request.env['guidance.request'].sudo().search([
            ('id', '=', guidance_id),
            ('student_id', '=', partner.id)
        ], limit=1)
        if not guidance:
            return request.not_found()
        
        # Load attachments dengan sudo untuk memastikan akses
        attachments = request.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'guidance.request'),
            ('res_id', '=', guidance.id)
        ])
        
        values = {
            'guidance': guidance, 
            'page_name': 'guidance_detail',
            'attachments': attachments
        }
        return request.render('bimbingan_mahasiswa.portal_guidance_detail', values)

    @http.route('/my/guidance/comment/<int:guidance_id>', type='http', auth="user", website=True, methods=['POST'], csrf=True)
    def portal_guidance_comment(self, guidance_id, **kw):
        partner = request.env.user.partner_id
        guidance = request.env['guidance.request'].search([
            ('id', '=', guidance_id),
            ('student_id', '=', partner.id)
        ], limit=1)
        if not guidance:
            return request.not_found()
        comment = kw.get('comment')
        if comment:
            request.env['guidance.note'].sudo().create({
                'guidance_id': guidance.id,
                'note': comment
            })
        return request.redirect(f'/my/guidance/{guidance_id}')
    
    @http.route('/my/guidance/attachment/<int:attachment_id>', type='http', auth="user", website=True)
    def portal_guidance_attachment(self, attachment_id, **kw):
        """Download attachment untuk guidance request milik user"""
        partner = request.env.user.partner_id
        
        # Get attachment
        attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
        if not attachment.exists():
            return request.not_found()
        
        # Check if attachment belongs to user's guidance request
        if attachment.res_model == 'guidance.request':
            guidance = request.env['guidance.request'].sudo().browse(attachment.res_id)
            if not guidance.exists() or guidance.student_id.id != partner.id:
                return request.not_found()
        else:
            return request.not_found()
        
        # Return file
        return request.make_response(
            base64.b64decode(attachment.datas),
            headers=[
                ('Content-Type', attachment.mimetype or 'application/octet-stream'),
                ('Content-Disposition', f'attachment; filename="{attachment.name}"'),
                ('Content-Length', len(base64.b64decode(attachment.datas)))
            ]
        )
    
    @http.route('/my/guidance/attachment/delete/<int:attachment_id>', type='http', auth="user", website=True, csrf=False)
    def portal_guidance_attachment_delete(self, attachment_id, **kw):
        """Delete attachment untuk guidance request milik user"""
        partner = request.env.user.partner_id
        
        # Get attachment
        attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
        if not attachment.exists():
            return request.not_found()
        
        # Check if attachment belongs to user's guidance request
        guidance_id = None
        if attachment.res_model == 'guidance.request':
            guidance = request.env['guidance.request'].sudo().browse(attachment.res_id)
            if not guidance.exists() or guidance.student_id.id != partner.id:
                return request.not_found()
            
            # Check if guidance can still be edited
            if guidance.status not in ['draft', 'submitted']:
                return request.redirect(f'/my/guidance/{guidance.id}')
            
            # Delete attachment
            guidance_id = guidance.id
            attachment.sudo().unlink()
            
            return request.redirect(f'/my/guidance/edit/{guidance_id}')
        
        return request.not_found()

    @http.route('/my/guidance/edit/<int:guidance_id>', type='http', auth="user", website=True, methods=['GET'])
    def portal_guidance_edit_form(self, guidance_id, **kw):
        partner = request.env.user.partner_id
        guidance = request.env['guidance.request'].sudo().search([
            ('id', '=', guidance_id),
            ('student_id', '=', partner.id),
            ('status', 'in', ['draft', 'submitted'])
        ], limit=1)
        if not guidance:
            return request.not_found()
        
        # Load attachments
        attachments = request.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'guidance.request'),
            ('res_id', '=', guidance.id)
        ])
        
        values = {
            'guidance': guidance, 
            'page_name': 'guidance_edit',
            'attachments': attachments
        }
        return request.render('bimbingan_mahasiswa.portal_guidance_edit', values)

    @http.route('/my/guidance/edit/<int:guidance_id>', type='http', auth="user", website=True, methods=['POST'])
    def portal_guidance_edit(self, guidance_id, **kw):
        partner = request.env.user.partner_id
        guidance = request.env['guidance.request'].search([
            ('id', '=', guidance_id),
            ('student_id', '=', partner.id),
            ('status', 'in', ['draft', 'submitted'])
        ], limit=1)
        if not guidance:
            return request.not_found()
        
        description = kw.get('description')
        if description:
            vals = {
                'description': description
            }
            guidance_date = kw.get('guidance_date')
            if guidance_date:
                vals['guidance_date'] = datetime.datetime.strptime(guidance_date, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
            
            # Handle new attachments
            attachments = request.httprequest.files.getlist('attachments')
            if attachments:
                attachment_ids = []
                for attachment in attachments:
                    if attachment.filename:
                        attachment_id = request.env['ir.attachment'].sudo().create({
                            'name': attachment.filename,
                            'type': 'binary',
                            'datas': base64.b64encode(attachment.read()),
                            'res_model': 'guidance.request',
                            'res_id': guidance.id
                        })
                        attachment_ids.append(attachment_id.id)
                if attachment_ids:
                    # Add to existing attachments
                    existing_ids = guidance.attachment_ids.ids
                    vals['attachment_ids'] = [(6, 0, existing_ids + attachment_ids)]
            
            guidance.sudo().write(vals)
        return request.redirect(f'/my/guidance/{guidance_id}')

    @http.route('/my/guidance/submit', type='http', auth="user", website=True, methods=['GET'])
    def portal_guidance_submit_form(self, **kw):
        return request.render('bimbingan_mahasiswa.portal_guidance_submit', {'page_name': 'guidance_submit'})

    @http.route('/my/guidance/submit', type='http', auth="user", website=True, methods=['POST'])
    def portal_guidance_submit(self, **kw):
        partner = request.env.user.partner_id
        guidance_type = kw.get('guidance_type')
        description = kw.get('description')
        if guidance_type and description:
            vals = {
                'student_id': partner.id,
                'guidance_type': guidance_type,
                'description': description
            }
            guidance_date = kw.get('guidance_date')
            if guidance_date:
                vals['guidance_date'] = datetime.datetime.strptime(guidance_date, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
            attachments = request.httprequest.files.getlist('attachments')
            if attachments:
                attachment_ids = []
                for attachment in attachments:
                    if attachment.filename:
                        attachment_id = request.env['ir.attachment'].sudo().create({
                            'name': attachment.filename,
                            'type': 'binary',
                            'datas': base64.b64encode(attachment.read()),
                            'res_model': 'guidance.request',
                            'res_id': False
                        })
                        attachment_ids.append(attachment_id.id)
                if attachment_ids:
                    vals['attachment_ids'] = [(6, 0, attachment_ids)]
            guidance = request.env['guidance.request'].sudo().create(vals)
            if 'attachment_ids' in vals:
                for att_id in vals['attachment_ids'][0][2]:
                    request.env['ir.attachment'].sudo().browse(att_id).write({'res_id': guidance.id})
        return request.redirect('/my/guidance')