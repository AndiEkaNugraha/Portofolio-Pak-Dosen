# -*- coding: utf-8 -*-
import logging
import traceback
from odoo import http
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.http import request

_logger = logging.getLogger(__name__)

class BahanAjarController(WebsiteBlog):
    @http.route([
        '/blog/bahan-ajar-1',
        '/blog/bahan-ajar-1/page/<int:page>',
        '/blog/bahan-ajar-1/tag/<string:tag>',
        '/blog/bahan-ajar-1/tag/<string:tag>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def blog(self, blog=None, tag=None, page=1, **opt):
        blog = request.env['blog.blog'].sudo().search([('name', '=', 'Bahan Ajar')], limit=1)
        if not blog:
            return request.not_found()
        return super().blog(blog=blog, tag=tag, page=page, **opt)

        if not material:
            return request.render('website.404')

        # Track view
        material.track_view()

        values = {
            'material': material,
            'main_object': material,  # For SEO
        }
        return request.render('bahan_ajar.material_detail', values)

    @http.route(['/bahan-ajar/<model("bahan.ajar.post"):material>/download'],
               type='http', auth='public', website=True)
    def download(self, material, **kwargs):
        """Download PDF file"""
        if not material.pdf_file or material.content_type != 'pdf':
            return request.render('website.404')

        # Track download
        material.track_download()

        return request.make_response(
            material.pdf_file,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename={material.pdf_filename}'),
            ]
        )

    @http.route('/bahan-ajar/form', auth='public', website=True, methods=['GET'])
    def bahan_ajar_form_page(self, **kw):
        """Halaman form untuk add bahan ajar"""
        material_type_options = [
            ('lecture_notes', 'Catatan Kuliah'),
            ('slide', 'Slide Presentasi'),
            ('assignment', 'Tugas/Soal'),
            ('reference', 'Referensi/Buku'),
            ('exercise', 'Latihan Soal'),
            ('other', 'Lainnya'),
        ]
        
        return request.render('bahan_ajar.bahan_ajar_form', {
            'material_type_options': material_type_options,
            'values': {},
            'error': None,
        })

    @http.route('/bahan-ajar/form/submit', auth='public', website=True, methods=['POST'], csrf=False)
    def bahan_ajar_form_submit(self, **kw):
        """Process form submission"""
        try:
            BlogPost = request.env['blog.post']
            Blog = request.env['blog.blog']
            
            # Get or create blog
            blog = Blog.sudo().search([('name', '=', 'Bahan Ajar')], limit=1)
            if not blog:
                blog = Blog.sudo().create({'name': 'Bahan Ajar'})
            
            # Prepare values
            values = {
                'name': kw.get('name', ''),
                'blog_id': blog.id,
                'material_type': kw.get('material_type', 'other'),
                'topic': kw.get('topic', ''),
                'target_audience': kw.get('target_audience', ''),
                'file_type': kw.get('file_type', 'link'),
                'estimated_time': float(kw.get('estimated_time', 0)) if kw.get('estimated_time') else 0,
                'teaser': kw.get('teaser', ''),
                'website_published': kw.get('is_published') == 'on',
            }
            
            # Handle file based on type
            if kw.get('file_type') == 'video':
                values['video_url'] = kw.get('content_url', '')
            elif kw.get('file_type') == 'link':
                values['web_resource_url'] = kw.get('content_url', '')
            
            # Validate required fields
            required_fields = ['name', 'material_type', 'topic', 'file_type']
            missing_fields = [field for field in required_fields if not values.get(field)]
            
            if missing_fields:
                return request.render('bahan_ajar.bahan_ajar_form', {
                    'error': f'Field wajib diisi: {", ".join(missing_fields)}',
                    'values': kw,
                    'material_type_options': [
                        ('lecture_notes', 'Catatan Kuliah'),
                        ('slide', 'Slide Presentasi'),
                        ('assignment', 'Tugas/Soal'),
                        ('reference', 'Referensi/Buku'),
                        ('exercise', 'Latihan Soal'),
                        ('other', 'Lainnya'),
                    ],
                })
            
            # Create record
            new_record = BlogPost.create(values)
            return request.redirect(f'/blog/bahan-ajar-1/{new_record.slug}')
            
        except Exception as e:
            _logger.error(f"Error in bahan_ajar_form_submit: {str(e)}\n{traceback.format_exc()}")
            return request.render('bahan_ajar.bahan_ajar_form', {
                'error': f'Error: {str(e)}',
                'values': kw,
                'material_type_options': [
                    ('lecture_notes', 'Catatan Kuliah'),
                    ('slide', 'Slide Presentasi'),
                    ('assignment', 'Tugas/Soal'),
                    ('reference', 'Referensi/Buku'),
                    ('exercise', 'Latihan Soal'),
                    ('other', 'Lainnya'),
                ],
            })