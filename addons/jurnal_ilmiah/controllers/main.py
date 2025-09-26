# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL


class JurnalController(http.Controller):

    @http.route(['/jurnal', '/jurnal/page/<int:page>'], type='http', auth="public", website=True)
    def jurnal_index(self, page=1, search='', category_id=None, indexing=None, year=None, **kw):
        """Main journal listing page - berbeda dari /blog"""
        
        domain = []
        
        # Search filter
        if search:
            domain += [
                '|', '|', '|',
                ('name', 'ilike', search),
                ('authors', 'ilike', search),
                ('journal_name', 'ilike', search),
                ('subject_area', 'ilike', search)
            ]
        
        # Category filter
        if category_id:
            domain.append(('blog_id', '=', int(category_id)))
        
        # Indexing filter
        if indexing == 'scopus':
            domain.append(('scopus_indexed', '=', True))
        elif indexing == 'wos':
            domain.append(('wos_indexed', '=', True))
        elif indexing == 'sinta':
            domain.append(('sinta_indexed', '=', True))
        elif indexing == 'doaj':
            domain.append(('doaj_indexed', '=', True))
        
        # Year filter
        if year:
            domain.append(('publication_year', '=', int(year)))
        
        # Get data
        JurnalPost = request.env['jurnal.post']
        JurnalBlog = request.env['jurnal.blog']
        
        posts = JurnalPost.search(domain, order='publication_date desc')
        categories = JurnalBlog.search([])
        
        # Pagination
        total = len(posts)
        per_page = 10
        pager = request.website.pager(
            url='/jurnal',
            total=total,
            page=page,
            step=per_page,
            url_args={'search': search, 'category_id': category_id, 'indexing': indexing, 'year': year}
        )
        
        posts_paged = posts[(page-1)*per_page:page*per_page]
        
        # Get available years for filter
        years = list(set(posts.mapped('publication_year')))
        years.sort(reverse=True)
        
        # Create keep object for URL handling
        keep = QueryURL('/jurnal', ['search', 'category_id', 'indexing', 'year'])
        
        values = {
            'posts': posts_paged,
            'categories': categories,
            'years': years,
            'pager': pager,
            'search': search,
            'category_id': int(category_id) if category_id else None,
            'indexing': indexing,
            'year': int(year) if year else None,
            'keep': keep,
            'total_posts': total,
        }
        
        return request.render('jurnal_ilmiah.jurnal_index', values)

    @http.route(['/jurnal/detail/<int:post_id>'], type='http', auth="public", website=True)
    def jurnal_post(self, post_id, **kw):
        """Individual journal article page"""
        
        post = request.env['jurnal.post'].browse(post_id)
        
        if not post.exists():
            return request.not_found()
        
        # Increment view counter (similar to blog)
        post.sudo().write({'visits': post.visits + 1})
        
        # Get related posts (same category, different post)
        related_posts = request.env['jurnal.post'].search([
            ('blog_id', '=', post.blog_id.id),
            ('id', '!=', post.id)
        ], limit=5, order='publication_date desc')
        
        values = {
            'post': post,
            'related_posts': related_posts,
        }
        
        return request.render('jurnal_ilmiah.jurnal_post_detail', values)

    @http.route(['/jurnal/kategori/<int:category_id>'], type='http', auth="public", website=True)
    def jurnal_category(self, category_id, page=1, **kw):
        """Category-specific journal listing"""
        
        category = request.env['jurnal.blog'].browse(category_id)
        
        if not category.exists():
            return request.not_found()
        
        domain = [
            ('blog_id', '=', category_id)
        ]
        
        posts = request.env['jurnal.post'].search(domain, order='publication_date desc')
        
        # Pagination
        total = len(posts)
        per_page = 10
        pager = request.website.pager(
            url=f'/jurnal/kategori/{category_id}',
            total=total,
            page=page,
            step=per_page
        )
        
        posts_paged = posts[(page-1)*per_page:page*per_page]
        
        values = {
            'category': category,
            'posts': posts_paged,
            'pager': pager,
            'total_posts': total,
        }
        
        return request.render('jurnal_ilmiah.jurnal_category', values)

    @http.route(['/jurnal/search'], type='http', auth="public", website=True)
    def jurnal_search(self, **kw):
        """Advanced search page"""
        
        categories = request.env['jurnal.blog'].search([])
        years = request.env['jurnal.post'].read_group(
            [],
            ['publication_year'],
            ['publication_year']
        )
        
        values = {
            'categories': categories,
            'years': sorted([y['publication_year'] for y in years if y['publication_year']], reverse=True),
        }
        
        return request.render('jurnal_ilmiah.jurnal_search', values)