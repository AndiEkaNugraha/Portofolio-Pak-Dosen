# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL


class ProdukPenelitianController(http.Controller):

    @http.route(['/produk-penelitian', '/produk-penelitian/page/<int:page>'], type='http', auth="public", website=True)
    def produk_penelitian_index(self, page=1, sortby='name', search='', filterby='all', **kw):
        """Halaman utama produk penelitian"""
        
        ProdukPost = request.env['produk.post']
        ProdukBlog = request.env['produk.blog']
        
        domain = [('website_published', '=', True)]
        
        # Filter berdasarkan pencarian
        if search:
            domain += ['|', '|', '|', '|', '|', '|',
                      ('name', 'ilike', search),
                      ('subtitle', 'ilike', search),
                      ('teaser', 'ilike', search),
                      ('principal_investigator', 'ilike', search),
                      ('team_members', 'ilike', search),
                      ('meta_keywords', 'ilike', search),
                      ('technology_ids.name', 'ilike', search)]
        
        # Filter berdasarkan kategori
        if filterby != 'all':
            if filterby == 'prototype':
                domain += [('development_status', '=', 'prototype')]
            elif filterby == 'product':
                domain += [('development_status', 'in', ['production', 'commercial'])]
            elif filterby == 'innovation':
                domain += [('development_status', 'in', ['concept', 'design'])]
            elif filterby == 'applied_research':
                domain += [('development_status', 'in', ['testing', 'pilot'])]
            elif filterby == 'basic_research':
                domain += [('trl_level', 'in', ['1', '2', '3'])]
        
        # Sorting
        order = 'name'
        if sortby == 'name':
            order = 'name'
        elif sortby == 'date':
            order = 'create_date desc'
        elif sortby == 'trl':
            order = 'trl_level desc'
        elif sortby == 'status':
            order = 'development_status'
        
        # Paginasi
        total = ProdukPost.search_count(domain)
        page_detail = request.website.pager(
            url='/produk-penelitian',
            url_args={'sortby': sortby, 'search': search, 'filterby': filterby},
            total=total,
            page=page,
            step=12,
        )
        
        # Ambil data produk
        products = ProdukPost.search(domain, order=order, limit=12, offset=page_detail['offset'])
        
        # Data untuk statistik
        total_products = ProdukPost.search_count([('website_published', '=', True)])
        prototype_count = ProdukPost.search_count([('website_published', '=', True), ('development_status', '=', 'prototype')])
        production_count = ProdukPost.search_count([('website_published', '=', True), ('development_status', 'in', ['production', 'commercial'])])
        high_trl_count = ProdukPost.search_count([('website_published', '=', True), ('trl_level', 'in', ['7', '8', '9'])])
        
        # Kategori untuk filter
        categories = ProdukBlog.search([])
        
        # URL helper untuk sorting dan filtering
        keep = QueryURL('/produk-penelitian', ['search', 'filterby', 'sortby'])
        
        values = {
            'products': products,
            'pager': page_detail,
            'search': search,
            'filterby': filterby,
            'sortby': sortby,
            'categories': categories,
            'keep': keep,
            'total_products': total_products,
            'prototype_count': prototype_count,
            'production_count': production_count,
            'high_trl_count': high_trl_count,
        }
        
        return request.render("produk_penelitian.produk_index", values)

    @http.route(['/produk-penelitian/<model("produk.post"):product>', 
                 '/produk-penelitian/detail/<string:slug>'], 
                type='http', auth="public", website=True)
    def produk_penelitian_detail(self, product=None, slug=None, **kw):
        """Detail produk penelitian"""
        
        # If slug is provided, find the product by slug
        if slug and not product:
            product = request.env['produk.post'].search([('slug', '=', slug), ('website_published', '=', True)], limit=1)
            if not product:
                return request.render('website.404')
        
        # If no product found, return 404
        if not product:
            return request.render('website.404')
        
        # Produk terkait (sama kategori atau tipe)
        related_domain = [
            ('website_published', '=', True),
            ('id', '!=', product.id),
            '|',
            ('blog_id', '=', product.blog_id.id),
            ('development_status', '=', product.development_status)
        ]
        related_products = request.env['produk.post'].search(related_domain, limit=6)
        
        values = {
            'post': product,
            'product': product,
            'related_products': related_products,
        }
        
        return request.render("produk_penelitian.produk_detail", values)

    @http.route(['/produk-penelitian/kategori/<model("produk.blog"):blog>',
                 '/produk-penelitian/kategori/<model("produk.blog"):blog>/page/<int:page>'], 
                type='http', auth="public", website=True)
    def produk_penelitian_category(self, blog, page=1, **kw):
        """Halaman kategori produk penelitian"""
        
        domain = [
            ('website_published', '=', True),
            ('blog_id', '=', blog.id)
        ]
        
        # Paginasi
        total = request.env['produk.post'].search_count(domain)
        page_detail = request.website.pager(
            url=f'/produk-penelitian/kategori/{blog.id}',
            total=total,
            page=page,
            step=12,
        )
        
        # Ambil data produk
        products = request.env['produk.post'].search(
            domain, 
            order='create_date desc', 
            limit=12, 
            offset=page_detail['offset']
        )
        
        values = {
            'products': products,
            'blog': blog,
            'pager': page_detail,
        }
        
        return request.render("produk_penelitian.category", values)

    @http.route(['/produk-penelitian/ajax/contact'], type='json', auth="public", website=True)
    def produk_contact_ajax(self, **kw):
        """AJAX endpoint untuk form kontak"""
        
        try:
            # Validasi data
            name = kw.get('name', '').strip()
            email = kw.get('email', '').strip()
            phone = kw.get('phone', '').strip()
            message = kw.get('message', '').strip()
            product_id = kw.get('product_id')
            
            if not all([name, email, message]):
                return {'status': 'error', 'message': 'Nama, email, dan pesan harus diisi'}
            
            # Buat lead/inquiry
            lead_vals = {
                'name': f"Inquiry Produk Penelitian - {name}",
                'contact_name': name,
                'email_from': email,
                'phone': phone,
                'description': message,
                'source_id': request.env.ref('crm.source_website').id if request.env.ref('crm.source_website', False) else False,
            }
            
            if product_id:
                product = request.env['produk.post'].browse(int(product_id))
                if product.exists():
                    lead_vals['name'] = f"Inquiry - {product.name}"
                    lead_vals['description'] = f"Produk: {product.name}\n\nPesan:\n{message}"
            
            # Buat lead jika modul CRM tersedia
            if 'crm.lead' in request.env:
                request.env['crm.lead'].sudo().create(lead_vals)
            
            return {'status': 'success', 'message': 'Pesan Anda telah terkirim. Kami akan segera menghubungi Anda.'}
            
        except Exception as e:
            return {'status': 'error', 'message': 'Terjadi kesalahan. Silakan coba lagi.'}

    @http.route(['/produk-penelitian/search'], type='http', auth="public", website=True)
    def produk_penelitian_search(self, **kw):
        """Pencarian produk penelitian"""
        search_term = kw.get('search', '').strip()
        
        if not search_term:
            return request.redirect('/produk-penelitian')
        
        return request.redirect(f'/produk-penelitian?search={search_term}')