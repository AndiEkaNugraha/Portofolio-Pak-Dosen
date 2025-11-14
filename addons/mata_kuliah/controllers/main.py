# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL


class MataKuliahController(http.Controller):

    @http.route(['/mata-kuliah'], type='http', auth="public", website=True)
    def mata_kuliah_academic_years(self, **kw):
        """Main page showing academic years"""
        
        AcademicYear = request.env['academic.year']
        academic_years = AcademicYear.search([('is_active', '=', True)], order='name desc')
        
        values = {
            'academic_years': academic_years,
        }
        
        return request.render('mata_kuliah.mata_kuliah_academic_years', values)

    @http.route(['/mata-kuliah/tahun/<int:year_id>', '/mata-kuliah/tahun/<int:year_id>/page/<int:page>'], 
                type='http', auth="public", website=True)
    def mata_kuliah_index(self, year_id, page=1, search='', category_id=None, semester=None, course_type=None, sks=None, sortby='name', **kw):
        """Course listing page for specific academic year"""
        
        AcademicYear = request.env['academic.year']
        MataKuliahPost = request.env['mata_kuliah.post']
        MataKuliahBlog = request.env['mata_kuliah.blog']
        
        # Get the academic year
        academic_year = AcademicYear.browse(year_id)
        if not academic_year.exists():
            return request.not_found()
        
        domain = [('academic_year_ids', 'in', [year_id])]
        
        # Search filter
        if search:
            domain += [
                '|', '|', '|', '|',
                ('name', 'ilike', search),
                ('course_code', 'ilike', search),
                ('subtitle', 'ilike', search),
                ('content', 'ilike', search),
                ('prerequisites', 'ilike', search)
            ]
        
        # Category filter
        if category_id:
            domain.append(('blog_id', '=', int(category_id)))
        
        # Semester filter
        if semester:
            domain.append(('semester', '=', semester))
        
        # Course type filter
        if course_type:
            domain.append(('course_type', '=', course_type))
        
        # SKS filter
        if sks:
            domain.append(('sks', '=', int(sks)))
        
        # Sorting
        sort_options = {
            'name': 'name asc',
            'course_code': 'course_code asc',
            'sks': 'sks asc',
        }
        order_by = sort_options.get(sortby, 'name asc')
        
        posts = MataKuliahPost.search(domain, order=order_by)
        categories = MataKuliahBlog.search([])
        
        # Pagination
        posts_per_page = 12
        total_posts = len(posts)
        pager = request.website.pager(
            url=f'/mata-kuliah/tahun/{year_id}',
            url_args={'search': search, 'category_id': category_id, 'semester': semester, 'course_type': course_type, 'sks': sks, 'sortby': sortby},
            total=total_posts,
            page=page,
            step=posts_per_page
        )
        
        offset = (page - 1) * posts_per_page
        posts_paginated = posts[offset:offset + posts_per_page]
        
        # Get filter options
        semesters = ['1', '2', '3', '4', '5', '6', '7', '8', 'odd', 'even', 'both']
        course_types = ['mandatory', 'elective', 'specialization']
        sks_options = sorted(list(set(MataKuliahPost.search([]).mapped('sks'))))
        
        # Get counts for statistics
        all_posts_year = MataKuliahPost.search([('academic_year_ids', 'in', [year_id])])
        stats = {
            'total_courses': len(all_posts_year),
            'active_courses': len(all_posts_year),  # All courses in this academic year are considered active
            'mandatory_courses': MataKuliahPost.search_count([('academic_year_ids', 'in', [year_id]), ('course_type', '=', 'mandatory')]),
            'elective_courses': MataKuliahPost.search_count([('academic_year_ids', 'in', [year_id]), ('course_type', '=', 'elective')]),
            'total_sks': sum(MataKuliahPost.search([('academic_year_ids', 'in', [year_id])]).mapped('sks')),
        }
        
        values = {
            'academic_year': academic_year,
            'posts': posts_paginated,
            'categories': categories,
            'pager': pager,
            'search': search,
            'category_id': int(category_id) if category_id else None,
            'semester': semester,
            'course_type': course_type,
            'sks': int(sks) if sks else None,
            'sortby': sortby,
            'semesters': semesters,
            'course_types': course_types,
            'sks_options': sks_options,
            'stats': stats,
        }
        
        return request.render('mata_kuliah.mata_kuliah_index', values)

    @http.route([
        '/mata-kuliah/kuliah/<int:post_id>',  # Fallback for old URLs
        '/mata-kuliah/kuliah/<slug>-<int:post_id>',  # SEO-friendly URL
    ], type='http', auth="public", website=True)
    def mata_kuliah_post(self, post_id, slug=None, **kw):
        """Individual course page"""

        post = request.env['mata_kuliah.post'].browse(post_id)

        if not post.exists():
            return request.not_found()

        # Increment view counter
        post.sudo().write({'visits': post.visits + 1})

        # Get related posts (courses that share academic years)
        related_posts = request.env['mata_kuliah.post'].search([
            ('academic_year_ids', 'in', post.academic_year_ids.ids),
            ('id', '!=', post.id)
        ], limit=6, order='name asc')

        values = {
            'post': post,
            'related_posts': related_posts,
        }

        return request.render('mata_kuliah.mata_kuliah_post_detail', values)

    @http.route(['/mata-kuliah/tahun/<int:year_id>/kategori/<int:category_id>'], type='http', auth="public", website=True)
    def mata_kuliah_category(self, year_id, category_id, page=1, **kw):
        """Category-specific course listing for specific academic year"""
        
        AcademicYear = request.env['academic.year']
        academic_year = AcademicYear.browse(year_id)
        if not academic_year.exists():
            return request.not_found()
        
        category = request.env['mata_kuliah.blog'].browse(category_id)
        if not category.exists():
            return request.not_found()
        
        domain = [
            ('academic_year_ids', 'in', [year_id]),
            ('blog_id', '=', category_id)
        ]
        
        posts = request.env['mata_kuliah.post'].search(domain, order='name asc')
        
        # Pagination
        total = len(posts)
        per_page = 12
        pager = request.website.pager(
            url=f'/mata-kuliah/tahun/{year_id}/kategori/{category_id}',
            total=total,
            page=page,
            step=per_page
        )
        
        posts_paged = posts[(page-1)*per_page:page*per_page]
        
        values = {
            'academic_year': academic_year,
            'category': category,
            'posts': posts_paged,
            'pager': pager,
            'total_posts': total,
        }
        
        return request.render('mata_kuliah.mata_kuliah_category', values)