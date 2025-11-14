# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class AcaraController(http.Controller):

    @http.route(['/acara', '/acara/page/<int:page>'], type='http', auth="public", website=True)
    def acara_index(self, page=1, **kw):
        """Acara Dosen listing page"""

        # Get search parameters
        search = kw.get('search', '')
        category_id = kw.get('category_id', '')
        acara_type_id = kw.get('acara_type_id', '')
        role = kw.get('role', '')
        sortby = kw.get('sortby', 'name')

        # Base domain for published posts
        domain = [('website_published', '=', True)]

        # Apply search filters
        if search:
            domain += [
                '|', '|', '|',
                ('name', 'ilike', search),
                ('organizer', 'ilike', search),
                ('location', 'ilike', search),
                ('keywords', 'ilike', search)
            ]

        if category_id:
            try:
                domain += [('blog_id', '=', int(category_id))]
            except ValueError:
                pass

        if acara_type_id:
            try:
                domain += [('acara_type_id', '=', int(acara_type_id))]
            except ValueError:
                pass

        if role:
            domain += [('role', '=', role)]
        
        # Sorting
        order = 'name'
        if sortby == 'name':
            order = 'name'
        elif sortby == 'date':
            order = 'event_date desc'
        elif sortby == 'status':
            order = 'status'
        
        # Get categories and acara types for filter
        categories = request.env['acara.blog'].search([('active', '=', True)])
        acara_types = request.env['acara.type'].search([('active', '=', True)], order='sequence')
        
        # Pagination
        total = request.env['acara.post'].search_count(domain)
        page_detail = request.website.pager(
            url='/acara',
            url_args={'sortby': sortby, 'search': search, 'category_id': category_id, 'acara_type_id': acara_type_id, 'role': role},
            total=total,
            page=page,
            step=12,
        )
        
        # Get acara posts
        posts = request.env['acara.post'].search(domain, order=order, limit=12, offset=page_detail['offset'])
        
        # Statistics
        all_posts = request.env['acara.post'].search([('website_published', '=', True)])
        stats = {
            'total_acara': len(all_posts),
            'completed_count': len(all_posts.filtered(lambda p: p.status == 'completed')),
            'ongoing_count': len(all_posts.filtered(lambda p: p.status == 'ongoing')),
            'upcoming_count': len(all_posts.filtered(lambda p: p.status == 'upcoming')),
        }
        
        values = {
            'posts': posts,
            'pager': page_detail,
            'categories': categories,
            'acara_types': acara_types,
            'stats': stats,
            'search': search,
            'category_id': category_id and int(category_id) or '',
            'acara_type_id': acara_type_id and int(acara_type_id) or '',
            'role': role,
            'sortby': sortby,
        }
        
        return request.render('acara_dosen.acara_index', values)

    @http.route([
        '/acara/detail/<int:post_id>',
        '/acara/detail/<string:slug>',
        '/acara/detail/<string:slug>-<int:post_id>'
    ], type='http', auth="public", website=True)
    def acara_detail(self, post_id=None, slug=None, **kw):
        """Acara Dosen detail page"""

        # Try to find post by ID first, then by slug
        if post_id:
            post = request.env['acara.post'].search([
                ('id', '=', post_id),
                ('website_published', '=', True)
            ], limit=1)
        elif slug:
            post = request.env['acara.post'].search([
                ('slug', '=', slug),
                ('website_published', '=', True)
            ], limit=1)
        else:
            return request.not_found()

        if not post:
            return request.not_found()

        # Get related posts (same category, different post)
        related_posts = request.env['acara.post'].search([
            ('blog_id', '=', post.blog_id.id),
            ('id', '!=', post.id),
            ('website_published', '=', True)
        ], limit=3, order='event_date desc')

        values = {
            'post': post,
            'related_posts': related_posts,
            'main_object': post,
        }

        return request.render('acara_dosen.acara_detail', values)

    @http.route(['/acara/kategori/<model("acara.blog"):blog>'],
                type='http', auth="public", website=True)
    def acara_category(self, blog, **kw):
        """Acara Dosen category page"""
        domain = [
            ('blog_id', '=', blog.id),
            ('website_published', '=', True)
        ]

        # Get posts for this category
        posts = request.env['acara.post'].search(
            domain,
            order='event_date desc'
        )

        values = {
            'blog': blog,
            'posts': posts,
        }

        return request.render('acara_dosen.acara_category', values)

    @http.route(['/acara/download/<int:post_id>'], type='http', auth="public", website=True)
    def acara_download_certificate(self, post_id, **kw):
        """Download sertifikat acara"""

        post = request.env['acara.post'].search([
            ('id', '=', post_id),
            ('website_published', '=', True),
            ('certificate_file', '!=', False)
        ], limit=1)

        if not post:
            return request.not_found()

        # Use Odoo's standard binary download URL
        download_url = f'/web/content/acara.post/{post.id}/certificate_file?download=true'
        return request.redirect(download_url)