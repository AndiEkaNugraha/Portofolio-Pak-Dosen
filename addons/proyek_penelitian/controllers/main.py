# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.tools import html_escape


class ProyekPenelitianController(http.Controller):

    @http.route(['/proyek-penelitian', '/proyek-penelitian/page/<int:page>'], type='http', auth="public", website=True)
    def index(self, page=1, search='', category=None, status=None, **kwargs):
        """Main page showing all research projects"""
        ProyekPost = request.env['proyek.penelitian.post']
        ProyekBlog = request.env['proyek.penelitian.blog']
        
        # Build domain for filtering
        domain = [('website_published', '=', True)]
        
        if search:
            domain += ['|', '|', '|',
                      ('name', 'ilike', search),
                      ('principal_investigator', 'ilike', search),
                      ('research_area', 'ilike', search),
                      ('keywords', 'ilike', search)]
        
        if category:
            blog = ProyekBlog.sudo().search([('name', '=', category)], limit=1)
            if blog:
                domain += [('blog_id', '=', blog.id)]
        
        if status:
            domain += [('status', '=', status)]
        
        # Get posts with pagination
        posts_per_page = 12
        total_posts = ProyekPost.sudo().search_count(domain)
        
        pager = request.website.pager(
            url='/proyek-penelitian',
            url_args={'search': search, 'category': category, 'status': status},
            total=total_posts,
            page=page,
            step=posts_per_page
        )
        
        posts = ProyekPost.sudo().search(domain, limit=posts_per_page, 
                                        offset=pager['offset'], order='start_date desc')
        
        # Get categories and featured posts for sidebar
        categories = ProyekBlog.sudo().search([('website_published', '=', True)], order='sequence, name')
        featured_posts = ProyekPost.sudo().search([
            ('website_published', '=', True), 
            ('is_featured', '=', True)
        ], limit=5, order='start_date desc')
        
        # SEO values
        page_title = "Proyek Penelitian"
        if search:
            page_title += f" - Pencarian: {search}"
        if category:
            page_title += f" - {category}"
            
        meta_description = "Jelajahi berbagai proyek penelitian aktif dan terdahulu dengan informasi lengkap tentang tim, pendanaan, luaran, dan dampak penelitian."
        
        values = {
            'posts': posts,
            'categories': categories,
            'featured_posts': featured_posts,
            'pager': pager,
            'search_term': search,
            'current_category': category,
            'current_status': status,
            'page_title': page_title,
            'meta_description': meta_description,
            'total_posts': total_posts,
        }
        
        return request.render('proyek_penelitian.proyek_penelitian_index', values)
    
    @http.route(['/proyek-penelitian/<string:slug>'], type='http', auth="public", website=True)
    def detail(self, slug, **kwargs):
        """Detail page for specific research project"""
        ProyekPost = request.env['proyek.penelitian.post']
        
        # Find post by slug
        post = ProyekPost.sudo().search([
            ('slug', '=', slug),
            ('website_published', '=', True)
        ], limit=1)
        
        if not post:
            return request.not_found()
        
        # Get related posts from same category
        related_posts = ProyekPost.sudo().search([
            ('blog_id', '=', post.blog_id.id),
            ('website_published', '=', True),
            ('id', '!=', post.id)
        ], limit=5, order='start_date desc')
        
        # SEO values
        page_title = post.meta_title or post.name
        meta_description = post.meta_description or post.teaser or f"Proyek penelitian {post.name} yang dipimpin oleh {post.principal_investigator}"
        meta_keywords = post.meta_keywords or post.keywords
        
        values = {
            'post': post,
            'related_posts': related_posts,
            'related_products': post.product_ids.sorted(lambda r: r.product_type),
            'page_title': page_title,
            'meta_description': meta_description,
            'meta_keywords': meta_keywords,
        }
        
        return request.render('proyek_penelitian.proyek_penelitian_detail', values)
    
    @http.route(['/proyek-penelitian/kategori/<string:category>'], type='http', auth="public", website=True)
    def category(self, category, page=1, **kwargs):
        """Category page showing projects from specific category"""
        return self.index(page=page, category=category, **kwargs)
    
    @http.route(['/proyek-penelitian/status/<string:status>'], type='http', auth="public", website=True)
    def status(self, status, page=1, **kwargs):
        """Status page showing projects with specific status"""
        return self.index(page=page, status=status, **kwargs)
    
    @http.route(['/proyek-penelitian/search'], type='http', auth="public", website=True)
    def search(self, search='', **kwargs):
        """Search page for research projects"""
        return self.index(search=search, **kwargs)
    
    @http.route(['/proyek-penelitian/api/projects'], type='json', auth="public", website=True)
    def api_projects(self, limit=10, offset=0, category=None, status=None):
        """JSON API endpoint for getting projects data"""
        ProyekPost = request.env['proyek.penelitian.post']
        
        domain = [('website_published', '=', True)]
        
        if category:
            domain += [('blog_id.name', '=', category)]
        if status:
            domain += [('status', '=', status)]
        
        posts = ProyekPost.sudo().search(domain, limit=limit, offset=offset, order='start_date desc')
        
        data = []
        for post in posts:
            data.append({
                'id': post.id,
                'name': post.name,
                'slug': post.slug,
                'principal_investigator': post.principal_investigator,
                'status': post.status,
                'start_date': post.start_date.strftime('%Y-%m-%d') if post.start_date else None,
                'end_date': post.end_date.strftime('%Y-%m-%d') if post.end_date else None,
                'funding_source': post.funding_source,
                'total_budget': post.total_budget,
                'research_area': post.research_area,
                'teaser': post.teaser,
                'category': post.blog_id.name,
                'is_featured': post.is_featured,
            })
        
        return {
            'projects': data,
            'total': ProyekPost.sudo().search_count(domain)
        }