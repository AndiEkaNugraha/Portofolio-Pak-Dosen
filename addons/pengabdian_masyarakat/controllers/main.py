# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class PengabdianController(http.Controller):

    @http.route(['/pengabdian', '/pengabdian/page/<int:page>'], type='http', auth="public", website=True)
    def pengabdian_index(self, page=1, **kw):
        """Kegiatan Pengabdian listing page"""
        
        # Get search parameters
        search = kw.get('search', '')
        category_id = kw.get('category_id', '')
        pengabdian_type_id = kw.get('pengabdian_type_id', '')
        sortby = kw.get('sortby', 'name')
        
        # Base domain for published posts
        domain = [('is_published', '=', True)]
        
        # Apply search filters
        if search:
            domain += [
                '|', '|', '|',
                ('name', 'ilike', search),
                ('coordinator', 'ilike', search),
                ('location', 'ilike', search),
                ('keywords', 'ilike', search)
            ]
            
        if category_id:
            try:
                domain += [('blog_id', '=', int(category_id))]
            except ValueError:
                pass
                
        if pengabdian_type_id:
            try:
                domain += [('pengabdian_type_id', '=', int(pengabdian_type_id))]
            except ValueError:
                pass
        
        # Sorting
        order = 'name'
        if sortby == 'name':
            order = 'name'
        elif sortby == 'date':
            order = 'implementation_date desc'
        elif sortby == 'status':
            order = 'status'
        
        # Get categories and pengabdian types for filter
        categories = request.env['pengabdian.blog'].search([])
        pengabdian_types = request.env['pengabdian.type'].search([('active', '=', True)], order='sequence')
        
        # Pagination
        total = request.env['pengabdian.post'].search_count(domain)
        page_detail = request.website.pager(
            url='/pengabdian',
            url_args={'sortby': sortby, 'search': search, 'category_id': category_id, 'pengabdian_type_id': pengabdian_type_id},
            total=total,
            page=page,
            step=12,
        )
        
        # Get pengabdian posts
        posts = request.env['pengabdian.post'].search(domain, order=order, limit=12, offset=page_detail['offset'])
        
        # Statistics
        all_posts = request.env['pengabdian.post'].search([('is_published', '=', True)])
        stats = {
            'total_pengabdian': len(all_posts),
            'completed_count': len(all_posts.filtered(lambda p: p.status == 'completed')),
            'ongoing_count': len(all_posts.filtered(lambda p: p.status == 'ongoing')),
        }
        
        values = {
            'posts': posts,
            'pager': page_detail,
            'categories': categories,
            'pengabdian_types': pengabdian_types,
            'stats': stats,
            'search': search,
            'category_id': category_id and int(category_id) or '',
            'pengabdian_type_id': pengabdian_type_id and int(pengabdian_type_id) or '',
            'sortby': sortby,
        }
        
        return request.render('pengabdian_masyarakat.pengabdian_index', values)

    @http.route([
        '/pengabdian/detail/<int:post_id>',
        '/pengabdian/detail/<string:slug>',
        '/pengabdian/detail/<string:slug>-<int:post_id>'
    ], type='http', auth="public", website=True)
    def pengabdian_detail(self, post_id=None, slug=None, **kw):
        """Kegiatan Pengabdian detail page"""
        
        # Try to find post by ID first, then by slug
        if post_id:
            post = request.env['pengabdian.post'].search([
                ('id', '=', post_id),
                ('is_published', '=', True)
            ], limit=1)
        elif slug:
            post = request.env['pengabdian.post'].search([
                ('slug', '=', slug),
                ('is_published', '=', True)
            ], limit=1)
        else:
            return request.not_found()
        
        if not post:
            return request.not_found()
        
        # Get related posts (same category, different post)
        related_posts = request.env['pengabdian.post'].search([
            ('blog_id', '=', post.blog_id.id),
            ('id', '!=', post.id),
            ('is_published', '=', True)
        ], limit=3, order='implementation_date desc')
        
        values = {
            'post': post,
            'related_posts': related_posts,
            'main_object': post,
        }
        
        return request.render('pengabdian_masyarakat.pengabdian_detail', values)

    @http.route(['/pengabdian/kategori/<model("pengabdian.blog"):blog>'], 
                type='http', auth="public", website=True)
    def pengabdian_category(self, blog, **kw):
        """Kegiatan Pengabdian category page"""
        domain = [
            ('blog_id', '=', blog.id),
            ('is_published', '=', True)
        ]
        
        # Get posts for this category
        posts = request.env['pengabdian.post'].search(
            domain,
            order='implementation_date desc'
        )
        
        values = {
            'blog': blog,
            'posts': posts,
        }
        
        return request.render('pengabdian_masyarakat.pengabdian_category', values)

    @http.route(['/pengabdian/download/<int:post_id>'], type='http', auth="public", website=True)
    def pengabdian_download_report(self, post_id, **kw):
        """Download laporan kegiatan pengabdian"""

        post = request.env['pengabdian.post'].search([
            ('id', '=', post_id),
            ('is_published', '=', True),
            ('report_file', '!=', False)
        ], limit=1)

        if not post:
            return request.not_found()

        # Use Odoo's standard binary download URL
        # This redirects to the standard Odoo binary content URL
        download_url = f'/web/content/pengabdian.post/{post.id}/report_file?download=true'
        return request.redirect(download_url)