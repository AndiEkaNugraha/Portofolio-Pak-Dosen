# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class GrupRisetController(http.Controller):

    @http.route(['/grup-riset', '/grup-riset/page/<int:page>'], type='http', auth="public", website=True, sitemap=True)
    def grup_riset_index(self, page=1, **kwargs):
        """Halaman utama grup riset"""
        
        # Get published posts
        domain = [('is_published', '=', True)]
        
        # Filter by category if specified
        if kwargs.get('category'):
            blog = request.env['grup.riset.blog'].sudo().search([
                ('name', 'ilike', kwargs.get('category'))
            ], limit=1)
            if blog:
                domain.append(('blog_id', '=', blog.id))
        
        # Search functionality
        search_term = kwargs.get('search')
        if search_term:
            domain.extend([
                '|', '|', '|',
                ('name', 'ilike', search_term),
                ('teaser', 'ilike', search_term),
                ('research_focus', 'ilike', search_term),
                ('research_keywords', 'ilike', search_term)
            ])
        
        posts = request.env['grup.riset.post'].sudo().search(
            domain, order='is_featured desc, date desc'
        )
        
        # Pagination
        posts_per_page = 6
        total_posts = len(posts)
        pager = request.website.pager(
            url='/grup-riset',
            total=total_posts,
            page=page,
            step=posts_per_page,
            url_args=kwargs
        )
        
        posts = posts[(page-1)*posts_per_page:page*posts_per_page]
        
        # Get categories for filter
        categories = request.env['grup.riset.blog'].sudo().search([
            ('is_published', '=', True)
        ], order='sequence, name')
        
        # Get featured posts for sidebar
        featured_posts = request.env['grup.riset.post'].sudo().search([
            ('is_published', '=', True),
            ('is_featured', '=', True)
        ], limit=3, order='date desc')
        
        values = {
            'posts': posts,
            'categories': categories,
            'featured_posts': featured_posts,
            'pager': pager,
            'search_term': search_term,
            'current_category': kwargs.get('category'),
            'page_title': 'Grup Riset & Laboratorium',
            'meta_description': 'Jelajahi grup riset dan laboratorium dengan berbagai fokus penelitian dan inovasi teknologi terdepan.',
        }
        
        return request.render('grup_riset.grup_riset_index', values)

    @http.route(['/grup-riset/<string:slug>'], type='http', auth="public", website=True, sitemap=True)
    def grup_riset_detail(self, slug, **kwargs):
        """Halaman detail grup riset"""
        
        post = request.env['grup.riset.post'].sudo().search([
            ('slug', '=', slug),
            ('is_published', '=', True)
        ], limit=1)
        
        if not post:
            return request.not_found()
        
        # Get related posts from same category
        related_posts = request.env['grup.riset.post'].sudo().search([
            ('blog_id', '=', post.blog_id.id),
            ('id', '!=', post.id),
            ('is_published', '=', True)
        ], limit=3, order='date desc')
        
        # Get other featured posts
        other_featured = request.env['grup.riset.post'].sudo().search([
            ('is_featured', '=', True),
            ('is_published', '=', True),
            ('id', '!=', post.id)
        ], limit=3, order='date desc')
        
        values = {
            'post': post,
            'related_posts': related_posts,
            'other_featured': other_featured,
            'page_title': post.meta_title or post.name,
            'meta_description': post.meta_description or post.teaser,
            'meta_keywords': post.meta_keywords,
        }
        
        return request.render('grup_riset.grup_riset_detail', values)

    @http.route(['/grup-riset/kategori/<string:category_slug>'], type='http', auth="public", website=True, sitemap=True)
    def grup_riset_category(self, category_slug, page=1, **kwargs):
        """Halaman kategori grup riset"""
        
        # Find category by slug-like matching
        category = request.env['grup.riset.blog'].sudo().search([
            ('name', 'ilike', category_slug.replace('-', ' ')),
            ('is_published', '=', True)
        ], limit=1)
        
        if not category:
            return request.not_found()
        
        # Get posts in this category
        posts = request.env['grup.riset.post'].sudo().search([
            ('blog_id', '=', category.id),
            ('is_published', '=', True)
        ], order='is_featured desc, date desc')
        
        # Pagination
        posts_per_page = 6
        total_posts = len(posts)
        pager = request.website.pager(
            url=f'/grup-riset/kategori/{category_slug}',
            total=total_posts,
            page=page,
            step=posts_per_page
        )
        
        posts = posts[(page-1)*posts_per_page:page*posts_per_page]
        
        values = {
            'posts': posts,
            'category': category,
            'pager': pager,
            'page_title': f'{category.name} - Grup Riset',
            'meta_description': f'Grup riset dan laboratorium dalam kategori {category.name}. {category.subtitle or ""}',
        }
        
        return request.render('grup_riset.grup_riset_category', values)

    @http.route(['/grup-riset/search'], type='http', auth="public", website=True)
    def grup_riset_search(self, **kwargs):
        """AJAX search untuk grup riset"""
        
        search_term = kwargs.get('term', '').strip()
        if not search_term:
            return request.jsonify([])
        
        posts = request.env['grup.riset.post'].sudo().search([
            ('is_published', '=', True),
            '|', '|', '|',
            ('name', 'ilike', search_term),
            ('teaser', 'ilike', search_term),
            ('research_focus', 'ilike', search_term),
            ('research_keywords', 'ilike', search_term)
        ], limit=5)
        
        results = []
        for post in posts:
            results.append({
                'label': post.name,
                'value': post.name,
                'url': f'/grup-riset/{post.slug}',
                'category': post.blog_id.name,
                'leader': post.leader_name
            })
        
        return request.jsonify(results)