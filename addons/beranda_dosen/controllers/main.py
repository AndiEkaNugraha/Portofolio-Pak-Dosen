# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class BerandaController(http.Controller):

    @http.route(['/', '/beranda', '/beranda/<string:slug>'], type='http', auth="public", website=True, sitemap=True)
    def beranda_homepage(self, slug=None, **kwargs):
        """Homepage controller for professor portfolio"""
        
        # Get profile based on slug or active profile
        if slug:
            profile = request.env['beranda.profile'].sudo().search([
                ('slug', '=', slug),
                ('is_active', '=', True)
            ], limit=1)
        else:
            profile = request.env['beranda.profile'].sudo().search([
                ('is_active', '=', True)
            ], limit=1, order='sequence, id')
        
        if not profile:
            # If no profile found, create a default message
            values = {
                'profile': None,
                'achievements': [],
                'recent_posts': [],
                'stats': {},
                'meta_title': 'Portofolio Dosen',
                'meta_description': 'Website portofolio profesional dosen',
            }
            return request.render('beranda_dosen.homepage_template', values)
        
        # Get highlighted achievements
        achievements = request.env['beranda.achievement'].sudo().search([
            ('profile_id', '=', profile.id),
            ('is_highlight', '=', True)
        ], limit=6, order='date desc, sequence')
        
        # Get recent posts from other modules (if available)
        recent_posts = []
        
        # Try to get recent jurnal posts
        try:
            jurnal_posts = request.env['jurnal.post'].sudo().search([
                ('is_published', '=', True)
            ], limit=3, order='date desc')
            recent_posts.extend([{
                'title': post.name,
                'date': post.date,
                'url': f'/jurnal/{post.slug}' if hasattr(post, 'slug') else '#',
                'type': 'Jurnal Ilmiah'
            } for post in jurnal_posts])
        except:
            pass
        
        # Try to get recent HKI posts
        try:
            hki_posts = request.env['hki.post'].sudo().search([
                ('is_published', '=', True)
            ], limit=3, order='date desc')
            recent_posts.extend([{
                'title': post.name,
                'date': post.date,
                'url': f'/hki/{post.slug}' if hasattr(post, 'slug') else '#',
                'type': 'HKI/Paten'
            } for post in hki_posts])
        except:
            pass
        
        # Try to get recent produk penelitian
        try:
            produk_posts = request.env['produk.post'].sudo().search([
                ('is_published', '=', True)
            ], limit=3, order='date desc')
            recent_posts.extend([{
                'title': post.name,
                'date': post.date,
                'url': f'/produk-penelitian/{post.slug}' if hasattr(post, 'slug') else '#',
                'type': 'Produk Penelitian'
            } for post in produk_posts])
        except:
            pass
        
        # Sort recent posts by date and limit to 6
        recent_posts = sorted(recent_posts, key=lambda x: x['date'], reverse=True)[:6]
        
        # Prepare statistics
        stats = {
            'publications': profile.total_publications or 0,
            'research_projects': profile.total_research_projects or 0,
            'patents': profile.total_patents or 0,
            'years_experience': profile.years_experience or 0,
            'h_index': profile.h_index or 0,
            'citations': profile.total_citations or 0,
        }
        
        # Prepare SEO data
        meta_title = profile.meta_title or f"{profile.display_name_with_title} - Portofolio Akademik"
        meta_description = profile.meta_description or profile.short_bio or f"Portofolio akademik {profile.name}"
        
        values = {
            'profile': profile,
            'achievements': achievements,
            'recent_posts': recent_posts,
            'stats': stats,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keywords': profile.meta_keywords,
        }
        
        return request.render('beranda_dosen.homepage_template', values)

    @http.route('/download-cv', type='http', auth="public", website=True)
    def download_cv(self, **kwargs):
        """Download CV endpoint"""
        
        profile = request.env['beranda.profile'].sudo().search([
            ('is_active', '=', True)
        ], limit=1)
        
        if not profile or not profile.cv_file:
            return request.not_found()
        
        # Return the file
        return request.make_response(
            profile.cv_file,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename="{profile.cv_filename or "CV.pdf"}"')
            ]
        )

    @http.route('/kontak-kolaborasi', type='http', auth="public", website=True, methods=['GET', 'POST'])
    def kontak_kolaborasi(self, **kwargs):
        """Contact form for collaboration"""
        
        profile = request.env['beranda.profile'].sudo().search([
            ('is_active', '=', True)
        ], limit=1)
        
        if not profile:
            return request.not_found()
        
        if request.httprequest.method == 'POST':
            # Handle form submission
            name = kwargs.get('name', '')
            email = kwargs.get('email', '')
            subject = kwargs.get('subject', '')
            message = kwargs.get('message', '')
            
            if name and email and message:
                # Send email or create lead/activity
                try:
                    # Create mail message
                    mail_values = {
                        'subject': f'Kolaborasi: {subject or "Tanpa Subjek"}',
                        'body_html': f"""
                            <p><strong>Pesan Kolaborasi Baru</strong></p>
                            <p><strong>Dari:</strong> {name} ({email})</p>
                            <p><strong>Subjek:</strong> {subject}</p>
                            <p><strong>Pesan:</strong></p>
                            <p>{message}</p>
                        """,
                        'email_from': email,
                        'email_to': profile.collaboration_email or profile.email,
                    }
                    
                    mail = request.env['mail.mail'].sudo().create(mail_values)
                    mail.send()
                    
                    return request.render('beranda_dosen.collaboration_success_template', {
                        'profile': profile,
                        'name': name
                    })
                    
                except Exception as e:
                    # Handle error
                    return request.render('beranda_dosen.collaboration_form_template', {
                        'profile': profile,
                        'error': 'Terjadi kesalahan saat mengirim pesan. Silakan coba lagi.',
                        'name': name,
                        'email': email,
                        'subject': subject,
                        'message': message,
                    })
            else:
                return request.render('beranda_dosen.collaboration_form_template', {
                    'profile': profile,
                    'error': 'Harap lengkapi semua field yang wajib diisi.',
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message,
                })
        
        return request.render('beranda_dosen.collaboration_form_template', {
            'profile': profile
        })