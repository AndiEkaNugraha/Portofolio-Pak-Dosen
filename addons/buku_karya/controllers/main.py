# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class BukuController(http.Controller):

    @http.route(['/buku', '/buku/page/<int:page>'], type='http', auth="public", website=True, sitemap=True)
    def buku_index(self, page=1, **kw):
        """Buku listing page"""
        
        # Get search parameters
        search = kw.get('search', '')
        category_id = kw.get('category_id', '')
        year = kw.get('year', '')
        
        # Base domain for published posts
        domain = [('is_published', '=', True)]
        
        # Apply search filters
        if search:
            domain += [
                '|', '|', '|', '|',
                ('name', 'ilike', search),
                ('authors', 'ilike', search),
                ('co_authors', 'ilike', search),
                ('subtitle', 'ilike', search),
                ('keywords', 'ilike', search)
            ]
            
        if category_id:
            try:
                domain += [('blog_id', '=', int(category_id))]
            except ValueError:
                pass
                
        if year:
            try:
                domain += [('publication_year', '=', int(year))]
            except ValueError:
                pass
        
        # Get categories and book types for filter
        categories = request.env['buku.blog'].sudo().search([])
        
        # Get unique publication years for filter
        all_books = request.env['buku.post'].sudo().search([('is_published', '=', True)], order='publication_year desc')
        years = sorted(list(set(book.publication_year for book in all_books if book.publication_year)), reverse=True)
        
        # Pagination setup
        POST_PER_PAGE = 12
        total_posts = request.env['buku.post'].sudo().search_count(domain)
        pager = request.website.pager(
            url='/buku',
            url_args=kw,
            total=total_posts,
            page=page,
            step=POST_PER_PAGE,
        )
        
        # Get posts for current page
        posts = request.env['buku.post'].sudo().search(
            domain, 
            order='publication_year desc, id desc',
            limit=POST_PER_PAGE,
            offset=pager['offset']
        )
        
        # Statistics
        published_books = request.env['buku.post'].sudo().search([('is_published', '=', True)])
        stats = {
            'total_books': len(published_books),
            'published_books': len(published_books.filtered(lambda p: p.status == 'published')),
        }
        
        values = {
            'posts': posts,
            'categories': categories,
            'years': years,
            'stats': stats,
            'search': search,
            'category_id': category_id and int(category_id) or '',
            'selected_year': year and int(year) or '',
            'pager': pager,
        }
        
        return request.render('buku_karya.buku_index', values)

    @http.route(['/buku/detail/<string:slug>'], type='http', auth="public", website=True, sitemap=True)
    def buku_detail(self, slug, **kw):
        """Book detail page"""
        
        # Try to find by slug first
        post = request.env['buku.post'].sudo().search([
            ('slug', '=', slug), 
            ('is_published', '=', True)
        ], limit=1)
        
        # If not found by slug, try by ID 
        if not post:
            try:
                post_id = int(slug.split('-')[-1]) if '-' in slug else int(slug)
                post = request.env['buku.post'].sudo().search([
                    ('id', '=', post_id),
                    ('is_published', '=', True)
                ], limit=1)
            except (ValueError, IndexError):
                pass
        
        if not post:
            return request.not_found()
        
        # Get related books (same category, different book)
        related_books = request.env['buku.post'].sudo().search([
            ('blog_id', '=', post.blog_id.id),
            ('id', '!=', post.id),
            ('is_published', '=', True)
        ], limit=4, order='publication_year desc')
        
        # Get books by same author
        author_books = request.env['buku.post'].sudo().search([
            ('authors', 'ilike', post.authors.split(',')[0].strip() if post.authors else ''),
            ('id', '!=', post.id),
            ('is_published', '=', True)
        ], limit=4, order='publication_year desc')
        
        values = {
            'post': post,
            'related_books': related_books,
            'author_books': author_books,
            'main_object': post,
        }
        
        return request.render('buku_karya.buku_detail', values)

    @http.route(['/buku/penulis/<string:author_name>'], type='http', auth="public", website=True, sitemap=True)
    def buku_by_author(self, author_name, **kw):
        """Books by author page"""
        
        posts = request.env['buku.post'].sudo().search([
            '|',
            ('authors', 'ilike', author_name),
            ('co_authors', 'ilike', author_name),
            ('is_published', '=', True)
        ], order='publication_year desc')
        
        values = {
            'posts': posts,
            'author_name': author_name,
            'page_name': f'Buku oleh: {author_name}',
        }
        
        return request.render('buku_karya.buku_index', values)

    @http.route(['/buku/tahun/<int:year>'], type='http', auth="public", website=True, sitemap=True)
    def buku_by_year(self, year, **kw):
        """Books by publication year"""
        
        posts = request.env['buku.post'].sudo().search([
            ('publication_year', '=', year),
            ('is_published', '=', True)
        ], order='publication_year desc')
        
        values = {
            'posts': posts,
            'year': year,
            'page_name': f'Buku Tahun {year}',
        }
        
        return request.render('buku_karya.buku_index', values)
        
    @http.route(['/buku/cari'], type='http', auth="public", website=True, methods=['GET'])
    def buku_search(self, **kw):
        """Search books page"""
        return self.buku_index(**kw)