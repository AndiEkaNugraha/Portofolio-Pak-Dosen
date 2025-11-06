# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class MatakuliahWebsite(http.Controller):
    """Controller untuk halaman website mata kuliah"""

    @http.route('/mata-kuliah', auth='public', website=True, sitemap=True)
    def mata_kuliah_list(self, **kwargs):
        """Halaman daftar mata kuliah"""
        courses = request.env['matakuliah.post'].sudo().search([
            ('website_published', '=', True)
        ], order='course_code asc')

        # Filtering berdasarkan parameter query
        search_query = kwargs.get('search', '')
        if search_query:
            courses = courses.filtered(lambda c: 
                search_query.lower() in c.course_name.lower() or 
                search_query.lower() in c.course_code.lower()
            )

        return request.render('matakuliah.matakuliah_list_template', {
            'courses': courses,
            'search_query': search_query,
            'pager_url': '/mata-kuliah',
        })

    @http.route('/mata-kuliah/<slug>', auth='public', website=True, sitemap=True)
    def mata_kuliah_detail(self, slug, **kwargs):
        """Halaman detail mata kuliah"""
        course = request.env['matakuliah.post'].sudo().search([
            ('slug', '=', slug),
            ('website_published', '=', True)
        ], limit=1)

        if not course:
            return request.render('website.404')

        return request.render('matakuliah.matakuliah_detail_template', {
            'course': course,
            'main_object': course,  # Untuk SEO
        })

    @http.route('/mata-kuliah/<slug>/download-silabus', auth='public', website=True)
    def download_silabus(self, slug, **kwargs):
        """Download file silabus mata kuliah"""
        course = request.env['matakuliah.post'].sudo().search([
            ('slug', '=', slug),
            ('website_published', '=', True)
        ], limit=1)

        if not course or not course.course_syllabus_file:
            return request.render('website.404')

        # Download file
        return request.make_response(
            course.course_syllabus_file,
            [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', 
                 f'attachment; filename="{course._get_image_filename()}"'),
            ]
        )

    @http.route('/mata-kuliah/search', auth='public', website=True, sitemap=True)
    def mata_kuliah_search(self, **kwargs):
        """Pencarian mata kuliah"""
        search_query = kwargs.get('q', '')
        
        if not search_query:
            return http.redirect_with_hash('/mata-kuliah')

        courses = request.env['matakuliah.post'].sudo().search([
            ('website_published', '=', True),
            '|',
            ('course_name', 'ilike', search_query),
            ('course_code', 'ilike', search_query),
        ], order='course_code asc')

        return request.render('matakuliah.matakuliah_list_template', {
            'courses': courses,
            'search_query': search_query,
            'pager_url': '/mata-kuliah/search',
        })

    @http.route('/mata-kuliah/by-type/<course_type>', auth='public', website=True, sitemap=True)
    def mata_kuliah_by_type(self, course_type, **kwargs):
        """Filter mata kuliah berdasarkan tipe"""
        courses = request.env['matakuliah.post'].sudo().search([
            ('course_type', '=', course_type),
            ('website_published', '=', True)
        ], order='course_code asc')

        return request.render('matakuliah.matakuliah_list_template', {
            'courses': courses,
            'filter_type': course_type,
        })
