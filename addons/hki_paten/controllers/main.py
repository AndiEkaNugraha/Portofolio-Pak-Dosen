# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class HkiController(http.Controller):

    @http.route(['/hki', '/hki/page/<int:page>'], type='http', auth="public", website=True)
    def hki_index(self, page=1, sortby='name', search='', filterby='all', **kw):
        """HKI dan Paten listing page"""
        
        # Get search parameters
        search = kw.get('search', '')
        category_id = kw.get('category_id', '')
        hki_type_id = kw.get('hki_type_id', '')
        
        # Base domain for published posts
        domain = [('is_published', '=', True)]
        
        # Apply search filters
        if search:
            domain += [
                '|', '|', '|',
                ('name', 'ilike', search),
                ('creators', 'ilike', search),
                ('applicant', 'ilike', search),
                ('keywords', 'ilike', search)
            ]
            
        if category_id:
            try:
                domain += [('blog_id', '=', int(category_id))]
            except ValueError:
                pass
                
        if hki_type_id:
            try:
                domain += [('hki_type_id', '=', int(hki_type_id))]
            except ValueError:
                pass
        
        # Sorting
        order = 'name'
        if sortby == 'name':
            order = 'name'
        elif sortby == 'date':
            order = 'application_date desc'
        elif sortby == 'type':
            order = 'hki_type_id'
        
        # Get categories and HKI types for filter
        categories = request.env['hki.blog'].search([])
        hki_types = request.env['hki.type'].search([('active', '=', True)], order='sequence')
        
        # Pagination
        total = request.env['hki.post'].search_count(domain)
        page_detail = request.website.pager(
            url='/hki',
            url_args={'sortby': sortby, 'search': search, 'category_id': category_id, 'hki_type_id': hki_type_id},
            total=total,
            page=page,
            step=12,
        )
        
        # Get HKI posts
        posts = request.env['hki.post'].search(domain, order=order, limit=12, offset=page_detail['offset'])
        
        # Statistics
        all_posts = request.env['hki.post'].search([('is_published', '=', True)])
        stats = {
            'total_hki': len(all_posts),
            'patent_count': len(all_posts.filtered(lambda p: p.hki_type_id.code in ['P', 'PS'])),
            'copyright_count': len(all_posts.filtered(lambda p: p.hki_type_id.code == 'HC')),
            'trademark_count': len(all_posts.filtered(lambda p: p.hki_type_id.code == 'M')),
        }
        
        values = {
            'posts': posts,
            'pager': page_detail,
            'categories': categories,
            'hki_types': hki_types,
            'stats': stats,
            'search': search,
            'category_id': category_id and int(category_id) or '',
            'hki_type_id': hki_type_id and int(hki_type_id) or '',
            'sortby': sortby,
        }
        
        return request.render('hki_paten.hki_index', values)

    @http.route(['/hki/detail/<string:slug>'], type='http', auth="public", website=True)
    def hki_detail(self, slug, **kw):
        """HKI detail page"""
        post = request.env['hki.post'].search([
            ('slug', '=', slug), 
            ('is_published', '=', True)
        ], limit=1)
        
        if not post:
            return request.not_found()
        
        # Get related posts (same category, different post)
        related_posts = request.env['hki.post'].search([
            ('blog_id', '=', post.blog_id.id),
            ('id', '!=', post.id),
            ('is_published', '=', True)
        ], limit=3, order='application_date desc')
        
        # Get similar posts (same HKI type, different post)
        similar_posts = request.env['hki.post'].search([
            ('hki_type_id', '=', post.hki_type_id.id),
            ('id', '!=', post.id),
            ('is_published', '=', True)
        ], limit=3, order='application_date desc')
        
        values = {
            'post': post,
            'related_posts': related_posts,
            'similar_posts': similar_posts,
            'main_object': post,
        }
        
        return request.render('hki_paten.hki_detail', values)

    @http.route(['/hki/kategori/<model("hki.blog"):blog>', '/hki/kategori/<model("hki.blog"):blog>/page/<int:page>'], 
                type='http', auth="public", website=True)
    def hki_category(self, blog, page=1, **kw):
        """HKI category page"""
        domain = [
            ('blog_id', '=', blog.id),
            ('status', 'in', ['published', 'granted', 'registered'])
        ]
        
        # Get posts for this category
        HkiPost = request.env['hki.post']
        total_posts = HkiPost.search_count(domain)
        
        # Pagination
        posts_per_page = 12
        pager = request.website.pager(
            url=f'/hki/kategori/{blog.id}',
            total=total_posts,
            page=page,
            step=posts_per_page,
        )
        
        posts = HkiPost.search(
            domain,
            order='application_date desc',
            limit=posts_per_page,
            offset=pager['offset']
        )
        
        values = {
            'blog': blog,
            'posts': posts,
            'pager': pager,
            'total_posts': total_posts,
        }
        
        return request.render('hki_paten.hki_category', values)

    @http.route(['/hki/search'], type='http', auth="public", website=True, methods=['GET', 'POST'])
    def hki_search(self, **kw):
        """Advanced HKI search page"""
        search_term = kw.get('search', '')
        hki_type_id = kw.get('hki_type_id', '')
        status = kw.get('status', '')
        year_from = kw.get('year_from', '')
        year_to = kw.get('year_to', '')
        category_id = kw.get('category_id', '')
        
        domain = [('status', 'in', ['published', 'granted', 'registered'])]
        
        if search_term:
            domain += [
                '|', '|', '|', '|',
                ('name', 'ilike', search_term),
                ('creators', 'ilike', search_term),
                ('technical_field', 'ilike', search_term),
                ('keywords', 'ilike', search_term)
            ]
        
        if hki_type_id:
            try:
                domain.append(('hki_type_id', '=', int(hki_type_id)))
            except ValueError:
                pass
        
        if status:
            domain.append(('status', '=', status))
            
        if category_id:
            domain.append(('blog_id', '=', int(category_id)))
        
        if year_from:
            domain.append(('application_year', '>=', int(year_from)))
            
        if year_to:
            domain.append(('application_year', '<=', int(year_to)))
        
        # Get results
        posts = request.env['hki.post'].search(domain, order='application_date desc', limit=50)
        
        # Get filter options
        categories = request.env['hki.blog'].search([])
        hki_types = request.env['hki.post']._fields['hki_type'].selection
        status_options = request.env['hki.post']._fields['status'].selection
        
        values = {
            'posts': posts,
            'categories': categories,
            'hki_types': hki_types,
            'status_options': status_options,
            'search_term': search_term,
            'hki_type_id': hki_type_id and int(hki_type_id) or '',
            'status': status,
            'year_from': year_from,
            'year_to': year_to,
            'category_id': int(category_id) if category_id else None,
        }
        
        return request.render('hki_paten.hki_search', values)

    @http.route(['/hki/statistik'], type='http', auth="public", website=True)
    def hki_statistics(self, **kw):
        """HKI statistics page"""
        HkiPost = request.env['hki.post']
        
        # Total counts by type
        type_stats = HkiPost.read_group(
            domain=[('status', 'in', ['published', 'granted', 'registered'])],
            fields=['hki_type_id'],
            groupby=['hki_type_id']
        )
        
        # Yearly statistics
        yearly_stats = HkiPost.read_group(
            domain=[('status', 'in', ['published', 'granted', 'registered'])],
            fields=['application_year'],
            groupby=['application_year'],
            orderby='application_year desc'
        )
        
        # Status statistics
        status_stats = HkiPost.read_group(
            domain=[],
            fields=['status'],
            groupby=['status']
        )
        
        # Office statistics
        office_stats = HkiPost.read_group(
            domain=[('status', 'in', ['published', 'granted', 'registered'])],
            fields=['registration_office_id'],
            groupby=['registration_office_id']
        )
        
        values = {
            'type_stats': type_stats,
            'yearly_stats': yearly_stats,
            'status_stats': status_stats,
            'office_stats': office_stats,
            'total_hki': sum([stat['hki_type_count'] for stat in type_stats]),
        }
        
        return request.render('hki_paten.hki_statistics', values)