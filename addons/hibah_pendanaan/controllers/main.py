# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class HibahPendanaanController(http.Controller):

    @http.route(['/hibah-pendanaan', '/hibah-pendanaan/page/<int:page>'], type='http', auth="public", website=True)
    def hibah_pendanaan_index(self, page=1, search='', category=None, status=None, **kwargs):
        """Display list of grants and funding"""
        domain = [('website_published', '=', True)]
        
        # Search filter
        if search:
            domain.append(['|', ('name', 'ilike', search), ('teaser', 'ilike', search)])
        
        # Category filter
        if category:
            try:
                category_id = int(category)
                domain.append(('blog_id', '=', category_id))
            except (ValueError, TypeError):
                pass
        
        # Status filter
        if status:
            domain.append(('status', '=', status))
        
        # Get grants
        grants = request.env['hibah.pendanaan.post'].search(domain, order='start_date desc')
        
        # Pagination
        grants_per_page = 12
        total_grants = len(grants)
        pager = request.website.pager(
            url='/hibah-pendanaan',
            total=total_grants,
            page=page,
            step=grants_per_page,
            url_args={'search': search, 'category': category, 'status': status}
        )
        
        grants = grants[(page-1) * grants_per_page:page * grants_per_page]
        
        # Get categories for filter
        categories = request.env['hibah.pendanaan.blog'].search([('website_published', '=', True)])
        
        # Get status options
        status_options = request.env['hibah.pendanaan.post']._fields['status'].selection
        
        values = {
            'grants': grants,
            'categories': categories,
            'status_options': status_options,
            'search': search,
            'current_category': int(category) if category else None,
            'current_status': status,
            'pager': pager,
            'total_grants': total_grants,
        }
        
        return request.render('hibah_pendanaan.grants_index', values)

    @http.route(['/hibah-pendanaan/<slug>'], type='http', auth="public", website=True)
    def hibah_pendanaan_detail(self, slug, **kwargs):
        """Display grant detail page"""
        grant = request.env['hibah.pendanaan.post'].search([
            ('slug', '=', slug),
            ('website_published', '=', True)
        ], limit=1)
        
        if not grant:
            return request.not_found()
        
        # Get related grants (same category, exclude current)
        related_grants = request.env['hibah.pendanaan.post'].search([
            ('blog_id', '=', grant.blog_id.id),
            ('website_published', '=', True),
            ('id', '!=', grant.id)
        ], limit=4, order='start_date desc')
        
        values = {
            'grant': grant,
            'related_grants': related_grants,
        }
        
        return request.render('hibah_pendanaan.grant_detail', values)

    @http.route(['/hibah-pendanaan/category/<int:category_id>'], type='http', auth="public", website=True)
    def hibah_pendanaan_category(self, category_id, page=1, **kwargs):
        """Display grants by category"""
        return self.hibah_pendanaan_index(page=page, category=str(category_id), **kwargs)

    @http.route(['/hibah-pendanaan/status/<status>'], type='http', auth="public", website=True)
    def hibah_pendanaan_status(self, status, page=1, **kwargs):
        """Display grants by status"""
        return self.hibah_pendanaan_index(page=page, status=status, **kwargs)

    @http.route(['/hibah-pendanaan/search'], type='http', auth="public", website=True)
    def hibah_pendanaan_search(self, search='', **kwargs):
        """Handle search functionality"""
        return self.hibah_pendanaan_index(search=search, **kwargs)

    @http.route(['/api/hibah-pendanaan'], type='json', auth="public", website=True)
    def hibah_pendanaan_api(self, **kwargs):
        """API endpoint for grants data"""
        domain = [('website_published', '=', True)]
        grants = request.env['hibah.pendanaan.post'].search(domain)
        
        result = []
        for grant in grants:
            result.append({
                'id': grant.id,
                'name': grant.name,
                'slug': grant.slug,
                'teaser': grant.teaser,
                'funding_agency': grant.funding_agency,
                'total_amount': grant.total_amount,
                'status': grant.status,
                'start_date': grant.start_date.strftime('%Y-%m-%d') if grant.start_date else None,
                'end_date': grant.end_date.strftime('%Y-%m-%d') if grant.end_date else None,
                'category': grant.blog_id.name,
                'is_featured': grant.is_featured,
            })
        
        return {
            'grants': result,
            'total': len(result)
        }