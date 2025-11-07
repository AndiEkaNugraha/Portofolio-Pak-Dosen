# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ReviewerController(http.Controller):

    @http.route(['/reviewer', '/reviewer/page/<int:page>'], type='http', auth="public", website=True)
    def reviewer_index(self, page=1, **kw):
        """Aktivitas Reviewer listing page"""
        
        # Get search parameters
        search = kw.get('search', '')
        category_id = kw.get('category_id', '')
        reviewer_type_id = kw.get('reviewer_type_id', '')
        review_level = kw.get('review_level', '')
        review_result = kw.get('review_result', '')
        
        # Base domain for published posts
        domain = [('is_published', '=', True)]
        
        # Apply search filters
        if search:
            domain += [
                '|', '|', '|',
                ('name', 'ilike', search),
                ('author_name', 'ilike', search),
                ('journal_conference_name', 'ilike', search),
                ('keywords', 'ilike', search)
            ]
            
        if category_id:
            try:
                domain += [('blog_id', '=', int(category_id))]
            except ValueError:
                pass
                
        if reviewer_type_id:
            try:
                domain += [('reviewer_type_id', '=', int(reviewer_type_id))]
            except ValueError:
                pass
        
        if review_level:
            domain += [('blog_id.review_level', '=', review_level)]
        
        if review_result:
            domain += [('review_result', '=', review_result)]
        
        # Get categories and reviewer types for filter
        categories = request.env['reviewer.blog'].search([])
        reviewer_types = request.env['reviewer.type'].search([('active', '=', True)], order='sequence')
        
        # Get reviewer posts
        posts = request.env['reviewer.post'].search(domain, order='review_date desc')
        
        # Statistics
        all_posts = request.env['reviewer.post'].search([('is_published', '=', True)])
        stats = {
            'total_reviews': len(all_posts),
            'completed_count': len(all_posts.filtered(lambda p: p.review_status == 'completed')),
            'in_progress_count': len(all_posts.filtered(lambda p: p.review_status == 'in_progress')),
            'international_count': len(all_posts.filtered(lambda p: p.blog_id.review_level == 'international')),
            'accept_count': len(all_posts.filtered(lambda p: p.review_result == 'accept')),
        }
        
        values = {
            'posts': posts,
            'categories': categories,
            'reviewer_types': reviewer_types,
            'stats': stats,
            'search': search,
            'category_id': category_id and int(category_id) or '',
            'reviewer_type_id': reviewer_type_id and int(reviewer_type_id) or '',
            'review_level': review_level,
            'review_result': review_result,
        }
        
        return request.render('reviewer_dosen.reviewer_index', values)

    @http.route([
        '/reviewer/detail/<int:post_id>',
        '/reviewer/detail/<string:slug>-<int:post_id>',
        '/reviewer/detail/<string:slug>'
    ], type='http', auth="public", website=True)
    def reviewer_detail(self, post_id=None, slug=None, **kw):
        """Aktivitas Reviewer detail page"""
        
        post = None
        
        # Try to find post by ID first (most reliable), then by slug
        if post_id:
            post = request.env['reviewer.post'].search([
                ('id', '=', post_id),
                ('is_published', '=', True)
            ], limit=1)
            
        # If not found by ID or no ID provided, try slug
        if not post and slug:
            post = request.env['reviewer.post'].search([
                ('slug', '=', slug),
                ('is_published', '=', True)
            ], limit=1)
        
        if not post:
            return request.not_found()
        
        # Get related posts (same category, different post)
        related_posts = request.env['reviewer.post'].search([
            ('blog_id', '=', post.blog_id.id),
            ('id', '!=', post.id),
            ('is_published', '=', True)
        ], limit=3, order='review_date desc')
        
        values = {
            'post': post,
            'related_posts': related_posts,
            'main_object': post,
        }
        
        return request.render('reviewer_dosen.reviewer_detail', values)

    @http.route(['/reviewer/kategori/<model("reviewer.blog"):blog>'], 
                type='http', auth="public", website=True)
    def reviewer_category(self, blog, **kw):
        """Aktivitas Reviewer category page"""
        domain = [
            ('blog_id', '=', blog.id),
            ('is_published', '=', True)
        ]
        
        # Get posts for this category
        posts = request.env['reviewer.post'].search(
            domain,
            order='review_date desc'
        )
        
        values = {
            'blog': blog,
            'posts': posts,
        }
        
        return request.render('reviewer_dosen.reviewer_category', values)

    @http.route(['/reviewer/download/<int:post_id>'], type='http', auth="public", website=True)
    def reviewer_download_document(self, post_id, **kw):
        """Download dokumen review"""

        post = request.env['reviewer.post'].search([
            ('id', '=', post_id),
            ('is_published', '=', True),
            ('review_document', '!=', False)
        ], limit=1)

        if not post:
            return request.not_found()

        # Use Odoo's standard binary download URL
        download_url = f'/web/content/reviewer.post/{post.id}/review_document?download=true'
        return request.redirect(download_url)
    
    @http.route(['/reviewer/certificate/<int:post_id>'], type='http', auth="public", website=True)
    def reviewer_download_certificate(self, post_id, **kw):
        """Download sertifikat review"""

        post = request.env['reviewer.post'].search([
            ('id', '=', post_id),
            ('is_published', '=', True),
            ('certificate_file', '!=', False)
        ], limit=1)

        if not post:
            return request.not_found()

        # Use Odoo's standard binary download URL
        download_url = f'/web/content/reviewer.post/{post.id}/certificate_file?download=true'
        return request.redirect(download_url)
