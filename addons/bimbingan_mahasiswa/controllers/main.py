# -*- coding: utf-8 -*-
import logging
import traceback
from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)


class BimbinganMahasiswaController(http.Controller):
    """Controller untuk website frontend Bimbingan Mahasiswa"""

    @http.route('/bimbingan-mahasiswa', auth='public', website=True, sitemap=True)
    def bimbingan_index(self, **kw):
        """Halaman list semua bimbingan mahasiswa yang published"""
        try:
            BimbinganMahasiswa = request.env['bimbingan.mahasiswa']
            
            # Get filter parameters from URL
            guidance_type = kw.get('guidance_type')
            status = kw.get('status')
            search = kw.get('search', '')
            
            # Base domain - only published records
            domain = [('is_published', '=', True)]
            
            # Apply filters
            if guidance_type:
                domain.append(('guidance_type', '=', guidance_type))
            if status:
                domain.append(('status', '=', status))
            if search:
                domain += [
                    '|', '|', '|',
                    ('name', 'ilike', search),
                    ('topic', 'ilike', search),
                    ('student_name', 'ilike', search),
                    ('study_program', 'ilike', search),
                ]
            
            # Get all records matching domain
            bimbingan_list = BimbinganMahasiswa.search(domain, order='guidance_date desc')
            
            # Get unique values for filter options
            all_types = BimbinganMahasiswa.search_read(
                domain=[('is_published', '=', True)],
                fields=['guidance_type'],
                limit=False
            )
            guidance_types = list(set([x['guidance_type'] for x in all_types if x['guidance_type']]))
            
            all_status = BimbinganMahasiswa.search_read(
                domain=[('is_published', '=', True)],
                fields=['status'],
                limit=False
            )
            statuses = list(set([x['status'] for x in all_status if x['status']]))
            
            # Get statistics
            total_count = BimbinganMahasiswa.search_count([('is_published', '=', True)])
            active_count = BimbinganMahasiswa.search_count([
                ('is_published', '=', True),
                ('status', '=', 'active')
            ])
            
            return request.render('bimbingan_mahasiswa.bimbingan_index', {
                'posts': bimbingan_list,
                'guidance_types': guidance_types,
                'statuses': statuses,
                'guidance_type': guidance_type,
                'status': status,
                'search': search,
                'total_count': total_count,
                'active_count': active_count,
            })
        except Exception as e:
            _logger.error(f"Error in bimbingan_index: {str(e)}\n{traceback.format_exc()}")
            raise

    @http.route('/bimbingan-mahasiswa/<slug>', auth='public', website=True, sitemap=True)
    def bimbingan_detail(self, slug, **kw):
        """Halaman detail satu bimbingan mahasiswa"""
        BimbinganMahasiswa = request.env['bimbingan.mahasiswa']
        
        # Get the record by slug
        post = BimbinganMahasiswa.search([
            ('slug', '=', slug),
            ('is_published', '=', True)
        ], limit=1)
        
        if not post:
            return request.redirect('/bimbingan-mahasiswa')
        
        return request.render('bimbingan_mahasiswa.bimbingan_detail', {
            'post': post,
        })

    @http.route('/bimbingan-mahasiswa/form', auth='public', website=True, methods=['GET'])
    def bimbingan_form_page(self, **kw):
        """Halaman form untuk add bimbingan mahasiswa"""
        guidance_type_options = [
            ('thesis', 'Skripsi/Tesis/Disertasi'),
            ('project', 'Proyek Akhir'),
            ('research', 'Riset/Penelitian'),
            ('academic', 'Bimbingan Akademik'),
            ('course', 'Bimbingan Mata Kuliah'),
            ('other', 'Lainnya'),
        ]
        
        academic_level_options = [
            ('s1', 'S1/Sarjana'),
            ('s2', 'S2/Magister'),
            ('s3', 'S3/Doktor'),
        ]
        
        guidance_output_options = [
            ('thesis', 'Thesis/Skripsi'),
            ('paper', 'Paper/Makalah'),
            ('prototype', 'Prototype'),
            ('publication', 'Publikasi'),
            ('patent', 'Patent'),
            ('other', 'Lainnya'),
        ]
        
        status_options = [
            ('active', 'Aktif'),
            ('completed', 'Selesai'),
            ('on_hold', 'On Hold'),
            ('pending', 'Pending'),
        ]
        
        return request.render('bimbingan_mahasiswa.bimbingan_form', {
            'guidance_type_options': guidance_type_options,
            'academic_level_options': academic_level_options,
            'guidance_output_options': guidance_output_options,
            'status_options': status_options,
            'values': {},
            'error': None,
        })

    @http.route('/bimbingan-mahasiswa/form/submit', auth='public', website=True, methods=['POST'], csrf=False)
    def bimbingan_form_submit(self, **kw):
        """Process form submission"""
        BimbinganMahasiswa = request.env['bimbingan.mahasiswa']
        
        try:
            values = {
                'name': kw.get('name', ''),
                'subtitle': kw.get('subtitle', ''),
                'student_name': kw.get('student_name', ''),
                'student_id': kw.get('student_id', ''),
                'student_email': kw.get('student_email', ''),
                'student_phone': kw.get('student_phone', ''),
                'study_program': kw.get('study_program', ''),
                'academic_level': kw.get('academic_level', 's1'),
                'guidance_type': kw.get('guidance_type', 'thesis'),
                'topic': kw.get('topic', ''),
                'description': kw.get('description', ''),
                'guidance_date': kw.get('guidance_date', False),
                'estimated_completion': kw.get('estimated_completion', False),
                'duration_months': int(kw.get('duration_months', 0)) if kw.get('duration_months') else 0,
                'status': kw.get('status', 'active'),
                'completion_percentage': int(kw.get('completion_percentage', 0)) if kw.get('completion_percentage') else 0,
                'guidance_output': kw.get('guidance_output', False),
                'guidance_notes': kw.get('guidance_notes', ''),
                'meeting_count': int(kw.get('meeting_count', 0)) if kw.get('meeting_count') else 0,
                'total_hours': int(kw.get('total_hours', 0)) if kw.get('total_hours') else 0,
                'meta_keywords': kw.get('meta_keywords', ''),
                'is_published': kw.get('is_published') == 'on',
            }
            
            required_fields = ['name', 'student_name', 'student_id', 'study_program', 'topic', 'guidance_date']
            missing_fields = [field for field in required_fields if not values.get(field)]
            
            if missing_fields:
                return request.render('bimbingan_mahasiswa.bimbingan_form', {
                    'error': f'Field wajib diisi: {", ".join(missing_fields)}',
                    'values': values,
                    'guidance_type_options': [('thesis', 'Skripsi/Tesis/Disertasi'), ('project', 'Proyek Akhir'), ('research', 'Riset/Penelitian'), ('academic', 'Bimbingan Akademik'), ('course', 'Bimbingan Mata Kuliah'), ('other', 'Lainnya')],
                    'academic_level_options': [('s1', 'S1/Sarjana'), ('s2', 'S2/Magister'), ('s3', 'S3/Doktor')],
                    'guidance_output_options': [('thesis', 'Thesis/Skripsi'), ('paper', 'Paper/Makalah'), ('prototype', 'Prototype'), ('publication', 'Publikasi'), ('patent', 'Patent'), ('other', 'Lainnya')],
                    'status_options': [('active', 'Aktif'), ('completed', 'Selesai'), ('on_hold', 'On Hold'), ('pending', 'Pending')],
                })
            
            new_record = BimbinganMahasiswa.create(values)
            return request.redirect(f'/bimbingan-mahasiswa/{new_record.slug}')
            
        except Exception as e:
            return request.render('bimbingan_mahasiswa.bimbingan_form', {
                'error': f'Error: {str(e)}',
                'values': kw,
                'guidance_type_options': [('thesis', 'Skripsi/Tesis/Disertasi'), ('project', 'Proyek Akhir'), ('research', 'Riset/Penelitian'), ('academic', 'Bimbingan Akademik'), ('course', 'Bimbingan Mata Kuliah'), ('other', 'Lainnya')],
                'academic_level_options': [('s1', 'S1/Sarjana'), ('s2', 'S2/Magister'), ('s3', 'S3/Doktor')],
                'guidance_output_options': [('thesis', 'Thesis/Skripsi'), ('paper', 'Paper/Makalah'), ('prototype', 'Prototype'), ('publication', 'Publikasi'), ('patent', 'Patent'), ('other', 'Lainnya')],
                'status_options': [('active', 'Aktif'), ('completed', 'Selesai'), ('on_hold', 'On Hold'), ('pending', 'Pending')],
            })

