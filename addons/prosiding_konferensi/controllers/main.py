# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL


class ProsidingController(http.Controller):

    @http.route(['/prosiding', '/prosiding/page/<int:page>'], type='http', auth="public", website=True)
    def prosiding_index(self, page=1, sortby='name', search='', category_id=None, indexing=None, year=None, publisher=None, **kw):
        """Main proceeding listing page - berbeda dari /blog"""
        
        domain = []
        
        # Search filter
        if search:
            domain += [
                '|', '|', '|', '|', '|',
                ('name', 'ilike', search),
                ('authors', 'ilike', search),
                ('conference_name', 'ilike', search),
                ('conference_acronym', 'ilike', search),
                ('subject_area', 'ilike', search),
                ('keywords', 'ilike', search)
            ]
        
        # Category filter
        if category_id:
            domain.append(('blog_id', '=', int(category_id)))
        
        # Indexing filter
        if indexing == 'ieee':
            domain.append(('ieee_indexed', '=', True))
        elif indexing == 'acm':
            domain.append(('acm_indexed', '=', True))
        elif indexing == 'scopus':
            domain.append(('scopus_indexed', '=', True))
        elif indexing == 'wos':
            domain.append(('wos_indexed', '=', True))
        elif indexing == 'sinta':
            domain.append(('sinta_indexed', '=', True))
        
        # Publisher filter
        if publisher:
            domain.append(('publisher', 'ilike', publisher))
        
        # Year filter
        if year:
            domain.append(('conference_year', '=', int(year)))
        
        # Sorting
        order = 'name'
        if sortby == 'name':
            order = 'name'
        elif sortby == 'date':
            order = 'conference_date desc'
        elif sortby == 'year':
            order = 'conference_year desc'
        
        # Get data
        ProsidingPost = request.env['prosiding.post']
        ProsidingBlog = request.env['prosiding.blog']
        
        # Pagination
        total = ProsidingPost.search_count(domain)
        page_detail = request.website.pager(
            url='/prosiding',
            url_args={'sortby': sortby, 'search': search, 'category_id': category_id, 'indexing': indexing, 'year': year, 'publisher': publisher},
            total=total,
            page=page,
            step=12,
        )
        
        posts = ProsidingPost.search(domain, order=order, limit=12, offset=page_detail['offset'])
        categories = ProsidingBlog.search([])
        
        # Get filter options
        years = ProsidingPost.search([]).mapped('conference_year')
        years = sorted(list(set(years)), reverse=True)
        
        publishers = ProsidingPost.search([]).mapped('publisher')
        publishers = sorted(list(set([p for p in publishers if p])))
        
        # Get counts for statistics
        all_posts = request.env['prosiding.post'].search([])
        stats = {
            'total_papers': len(all_posts),
            'ieee_papers': ProsidingPost.search_count([('ieee_indexed', '=', True)]),
            'acm_papers': ProsidingPost.search_count([('acm_indexed', '=', True)]),
            'scopus_papers': ProsidingPost.search_count([('scopus_indexed', '=', True)]),
            'international_papers': ProsidingPost.search_count([('blog_id.conference_scope', 'in', ['international', 'both'])]),
        }
        
        values = {
            'posts': posts,
            'categories': categories,
            'pager': page_detail,
            'search': search,
            'category_id': int(category_id) if category_id else None,
            'indexing': indexing,
            'year': int(year) if year else None,
            'publisher': publisher,
            'years': years,
            'publishers': publishers,
            'stats': stats,
            'sortby': sortby,
            'page_name': 'prosiding_index',
        }
        
        return request.render('prosiding_konferensi.prosiding_index', values)
    
    @http.route(['/prosiding/kategori/<int:category_id>', '/prosiding/kategori/<int:category_id>/page/<int:page>'], 
                type='http', auth="public", website=True)
    def prosiding_category(self, category_id, page=1, search='', **kw):
        """Category specific page"""
        return self.prosiding_index(page=page, search=search, category_id=category_id, **kw)
    
    @http.route(['/prosiding/paper/<slug>', '/prosiding/paper/<int:post_id>'], 
                type='http', auth="public", website=True)
    def prosiding_detail(self, slug=None, post_id=None, **kw):
        """Individual paper detail page"""
        
        ProsidingPost = request.env['prosiding.post']
        
        if slug:
            post = ProsidingPost.search([('slug', '=', slug)], limit=1)
            if not post:
                return request.not_found()
        elif post_id:
            post = ProsidingPost.browse(post_id)
            if not post.exists():
                return request.not_found()
        else:
            return request.not_found()
        
        # SEO canonical URL redirect if slug doesn't match (for fallback routes)
        if post.slug and slug != post.slug:
            return request.redirect(f'/prosiding/paper/{post.slug}', code=301)
        
        # Get related papers (same conference or category)
        related_domain = [
            ('id', '!=', post.id),
            '|',
            ('conference_name', '=', post.conference_name),
            ('blog_id', '=', post.blog_id.id)
        ]
        related_posts = ProsidingPost.search(related_domain, limit=6, order='conference_date desc')
        
        values = {
            'post': post,
            'related_posts': related_posts,
            'page_name': 'prosiding_detail',
            'main_object': post,
        }
        
        return request.render('prosiding_konferensi.prosiding_detail', values)
    
    @http.route('/prosiding/search/autocomplete', type='json', auth="public", website=True)
    def prosiding_search_autocomplete(self, term, **kw):
        """Autocomplete for search functionality"""
        
        ProsidingPost = request.env['prosiding.post']
        
        # Search in paper titles, conference names, and authors
        domain = [
            '|', '|', '|',
            ('name', 'ilike', term),
            ('conference_name', 'ilike', term),
            ('conference_acronym', 'ilike', term),
            ('authors', 'ilike', term)
        ]
        
        posts = ProsidingPost.search(domain, limit=10)
        
        suggestions = []
        for post in posts:
            suggestions.append({
                'label': post.name,
                'value': post.name,
                'url': post.website_url,
                'conference': post.conference_name,
                'year': post.conference_year,
            })
        
        return suggestions
    
    @http.route('/prosiding/statistics', type='http', auth="public", website=True)
    def prosiding_statistics(self, **kw):
        """Statistics page for proceedings"""
        
        ProsidingPost = request.env['prosiding.post']
        ProsidingBlog = request.env['prosiding.blog']
        
        # Get various statistics
        stats = {
            'total_papers': ProsidingPost.search_count([]),
            'total_categories': ProsidingBlog.search_count([]),
        }
        
        # Papers by year
        papers_by_year = {}
        years = ProsidingPost.search([]).mapped('conference_year')
        for year in set(years):
            if year:
                papers_by_year[year] = ProsidingPost.search_count([('conference_year', '=', year)])
        
        # Papers by indexing
        indexing_stats = {
            'IEEE Xplore': ProsidingPost.search_count([('ieee_indexed', '=', True)]),
            'ACM Digital Library': ProsidingPost.search_count([('acm_indexed', '=', True)]),
            'Scopus': ProsidingPost.search_count([('scopus_indexed', '=', True)]),
            'Web of Science': ProsidingPost.search_count([('wos_indexed', '=', True)]),
            'SINTA': ProsidingPost.search_count([('sinta_indexed', '=', True)]),
        }
        
        # Papers by category
        category_stats = {}
        categories = ProsidingBlog.search([])
        for category in categories:
            category_stats[category.name] = ProsidingPost.search_count([('blog_id', '=', category.id)])
        
        # Recent papers
        recent_papers = ProsidingPost.search([], order='conference_date desc', limit=5)
        
        values = {
            'stats': stats,
            'papers_by_year': dict(sorted(papers_by_year.items(), reverse=True)),
            'indexing_stats': indexing_stats,
            'category_stats': category_stats,
            'recent_papers': recent_papers,
            'page_name': 'prosiding_statistics',
        }
        
        return request.render('prosiding_konferensi.prosiding_statistics', values)