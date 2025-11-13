# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ProfileController(http.Controller):

    @http.route(['/profile'], type='http', auth="public", website=True)
    def profile_index(self, **kw):
        """Profile page - Display main profile directly"""
        
        # Get the main published profile (should be only one)
        post = request.env['profile.post'].sudo().search([
            ('is_published', '=', True),
            ('blog_id.is_main_profile', '=', True)
        ], limit=1)
        
        # If no main profile found, get the first published profile
        if not post:
            post = request.env['profile.post'].sudo().search([
                ('is_published', '=', True)
            ], order='sequence, id desc', limit=1)
        
        if not post:
            # No profile found, show empty page
            return request.render('profile_dosen.profile_empty')
        
        # Prepare all data for the profile page
        from datetime import date
        
        values = {
            'post': post,
            'main_object': post,
            'education': post.education_ids.filtered(lambda e: e.active).sorted(
                key=lambda e: (e.end_year or 9999, e.start_year), reverse=True
            ),  # Show all
            'work_experience': post.work_ids.filtered(lambda w: w.active).sorted(
                key=lambda w: (w.end_date or date(9999, 12, 31), w.start_date), reverse=True
            ),  # Show all
            'awards': post.award_ids.filtered(lambda a: a.active).sorted(
                key=lambda a: (a.award_date or date(1900, 1, 1)), reverse=True
            ),  # Show all
            'expertise': post.expertise_ids.filtered(lambda e: e.active).sorted(
                key=lambda e: e.sequence
            ),  # Show all
        }
        
        # Get counts for profile sections
        values['total_education'] = len(post.education_ids.filtered(lambda e: e.active))
        values['total_work'] = len(post.work_ids.filtered(lambda w: w.active))
        values['total_awards'] = len(post.award_ids.filtered(lambda a: a.active))
        values['total_expertise'] = len(post.expertise_ids.filtered(lambda e: e.active))
        
        # Fetch data from all addon modules with error handling
        # Limit to 9 items per category for profile page
        try:
            # Publications (Jurnal Ilmiah)
            values['publications_count'] = request.env['jurnal.post'].sudo().search_count([('is_published', '=', True)])
            values['publications'] = request.env['jurnal.post'].sudo().search(
                [('is_published', '=', True)], 
                order='publication_date desc', 
                limit=9
            )
        except:
            values['publications_count'] = 0
            values['publications'] = []
            
        try:
            # Books (Buku Karya)
            values['books_count'] = request.env['buku.post'].sudo().search_count([('is_published', '=', True)])
            values['books'] = request.env['buku.post'].sudo().search(
                [('is_published', '=', True)], 
                order='publication_year desc', 
                limit=9
            )
        except:
            values['books_count'] = 0
            values['books'] = []
            
        try:
            # Patents/HKI
            values['patents_count'] = request.env['hki.post'].sudo().search_count([('is_published', '=', True)])
            values['patents'] = request.env['hki.post'].sudo().search(
                [('is_published', '=', True)], 
                order='application_date desc', 
                limit=9
            )
            values['iprs'] = values['patents']  # Alias for template
            values['iprs_count'] = values['patents_count']
        except:
            values['patents_count'] = 0
            values['patents'] = []
            values['iprs'] = []
            values['iprs_count'] = 0
            
        try:
            # Research Projects
            values['projects_count'] = request.env['proyek.penelitian.post'].sudo().search_count([('is_published', '=', True)])
            values['projects'] = request.env['proyek.penelitian.post'].sudo().search(
                [('is_published', '=', True)], 
                order='start_date desc', 
                limit=9
            )
        except:
            values['projects_count'] = 0
            values['projects'] = []
            
        try:
            # Community Service
            values['community_count'] = request.env['pengabdian.post'].sudo().search_count([('is_published', '=', True)])
            values['community'] = request.env['pengabdian.post'].sudo().search(
                [('is_published', '=', True)], 
                order='implementation_date desc', 
                limit=9
            )
        except:
            values['community_count'] = 0
            values['community'] = []
            
        try:
            # Conferences
            values['conferences_count'] = request.env['prosiding.post'].sudo().search_count([('is_published', '=', True)])
            values['conferences'] = request.env['prosiding.post'].sudo().search(
                [('is_published', '=', True)], 
                order='conference_date desc', 
                limit=9
            )
        except:
            values['conferences_count'] = 0
            values['conferences'] = []
            
        try:
            # Grants (Hibah Pendanaan) - uses website_published field
            values['grants_count'] = request.env['hibah.pendanaan.post'].sudo().search_count([('website_published', '=', True)])
            values['grants'] = request.env['hibah.pendanaan.post'].sudo().search(
                [('website_published', '=', True)], 
                order='start_date desc', 
                limit=9
            )
        except:
            values['grants_count'] = 0
            values['grants'] = []
            
        try:
            # Products (Produk Penelitian)
            values['products_count'] = request.env['produk.post'].sudo().search_count([('is_published', '=', True)])
            values['products'] = request.env['produk.post'].sudo().search(
                [('is_published', '=', True)], 
                order='create_date desc', 
                limit=9
            )
        except:
            values['products_count'] = 0
            values['products'] = []
            
        try:
            # Research Groups (Grup Riset)
            values['groups_count'] = request.env['grup.riset.post'].sudo().search_count([('is_published', '=', True)])
            values['groups'] = request.env['grup.riset.post'].sudo().search(
                [('is_published', '=', True)], 
                order='create_date desc', 
                limit=9
            )
        except:
            values['groups_count'] = 0
            values['groups'] = []
            
        try:
            # Acara Dosen
            values['events_count'] = request.env['acara.post'].sudo().search_count([('is_published', '=', True)])
            values['events'] = request.env['acara.post'].sudo().search(
                [('is_published', '=', True)], 
                order='event_date desc', 
                limit=9
            )
        except:
            values['events_count'] = 0
            values['events'] = []
            
        try:
            # Reviewer Activities
            values['reviewer_count'] = request.env['reviewer.post'].sudo().search_count([('is_published', '=', True)])
            values['reviewer'] = request.env['reviewer.post'].sudo().search(
                [('is_published', '=', True)], 
                order='review_date desc', 
                limit=9
            )
        except:
            values['reviewer_count'] = 0
            values['reviewer'] = []
        
        # Prepare chart data (count by year starting from earliest data per category)
        from datetime import datetime, date
        
        current_year = datetime.now().year
        
        # Helper function to get years for a specific category
        def get_years_for_category(min_year):
            """Generate year range from min_year to current year"""
            if min_year:
                return list(range(min_year, current_year + 1))
            return [current_year]
        
        # Research chart data (groups + projects + grants)
        research_years_found = []
        try:
            group = request.env['grup.riset.post'].sudo().search([('is_published', '=', True)], order='create_date asc', limit=1)
            if group and group.create_date:
                research_years_found.append(group.create_date.year)
        except:
            pass
        try:
            project = request.env['proyek.penelitian.post'].sudo().search([('is_published', '=', True)], order='start_date asc', limit=1)
            if project and project.start_date:
                research_years_found.append(project.start_date.year)
        except:
            pass
        try:
            grant = request.env['hibah.pendanaan.post'].sudo().search([('website_published', '=', True)], order='start_date asc', limit=1)
            if grant and grant.start_date:
                research_years_found.append(grant.start_date.year)
        except:
            pass
        
        research_years = get_years_for_category(min(research_years_found) if research_years_found else None)
        research_data = []
        for year in research_years:
            count = 0
            # Count groups created in this year
            count += request.env['grup.riset.post'].sudo().search_count([
                ('is_published', '=', True),
                ('create_date', '>=', f'{year}-01-01'),
                ('create_date', '<=', f'{year}-12-31')
            ])
            # Count projects started in this year
            count += request.env['proyek.penelitian.post'].sudo().search_count([
                ('is_published', '=', True),
                ('start_date', '>=', date(year, 1, 1)),
                ('start_date', '<=', date(year, 12, 31))
            ])
            # Count grants in this year
            count += request.env['hibah.pendanaan.post'].sudo().search_count([
                ('website_published', '=', True),
                ('start_date', '>=', date(year, 1, 1)),
                ('start_date', '<=', date(year, 12, 31))
            ])
            research_data.append(count)
        
        values['research_chart'] = {
            'labels': research_years,
            'data': research_data
        }
        
        # Publications chart data (journals + conferences + books + iprs + products)
        publications_years_found = []
        try:
            journal = request.env['jurnal.post'].sudo().search([('is_published', '=', True)], order='publication_year asc', limit=1)
            if journal and journal.publication_year:
                publications_years_found.append(journal.publication_year)
        except:
            pass
        try:
            conf = request.env['prosiding.post'].sudo().search([('is_published', '=', True)], order='conference_date asc', limit=1)
            if conf and conf.conference_date:
                publications_years_found.append(conf.conference_date.year)
        except:
            pass
        try:
            book = request.env['buku.post'].sudo().search([('is_published', '=', True)], order='publication_year asc', limit=1)
            if book and book.publication_year:
                publications_years_found.append(book.publication_year)
        except:
            pass
        try:
            hki = request.env['hki.post'].sudo().search([('is_published', '=', True)], order='registration_date asc', limit=1)
            if hki and hki.registration_date:
                publications_years_found.append(hki.registration_date.year)
        except:
            pass
        try:
            prod = request.env['produk.post'].sudo().search([('is_published', '=', True)], order='development_date asc', limit=1)
            if prod and prod.development_date:
                publications_years_found.append(prod.development_date.year)
        except:
            pass
        
        publications_years = get_years_for_category(min(publications_years_found) if publications_years_found else None)
        publications_data = []
        for year in publications_years:
            count = 0
            # Count journal articles
            count += request.env['jurnal.post'].sudo().search_count([
                ('is_published', '=', True),
                ('publication_year', '=', year)
            ])
            # Count conferences
            count += request.env['prosiding.post'].sudo().search_count([
                ('is_published', '=', True),
                ('conference_date', '>=', date(year, 1, 1)),
                ('conference_date', '<=', date(year, 12, 31))
            ])
            # Count books
            count += request.env['buku.post'].sudo().search_count([
                ('is_published', '=', True),
                ('publication_year', '=', year)
            ])
            # Count HKI
            count += request.env['hki.post'].sudo().search_count([
                ('is_published', '=', True),
                ('registration_date', '>=', date(year, 1, 1)),
                ('registration_date', '<=', date(year, 12, 31))
            ])
            # Count products
            count += request.env['produk.post'].sudo().search_count([
                ('is_published', '=', True),
                ('development_date', '>=', date(year, 1, 1)),
                ('development_date', '<=', date(year, 12, 31))
            ])
            publications_data.append(count)
        
        values['publications_chart'] = {
            'labels': publications_years,
            'data': publications_data
        }
        
        # Community chart data (community services + events)
        community_years_found = []
        try:
            comm = request.env['pengabdian.post'].sudo().search([('is_published', '=', True)], order='implementation_date asc', limit=1)
            if comm and comm.implementation_date:
                community_years_found.append(comm.implementation_date.year)
        except:
            pass
        try:
            event = request.env['acara.post'].sudo().search([('is_published', '=', True)], order='event_date asc', limit=1)
            if event and event.event_date:
                community_years_found.append(event.event_date.year)
        except:
            pass
        
        community_years = get_years_for_category(min(community_years_found) if community_years_found else None)
        community_data = []
        for year in community_years:
            count = 0
            # Count community services
            count += request.env['pengabdian.post'].sudo().search_count([
                ('is_published', '=', True),
                ('implementation_date', '>=', date(year, 1, 1)),
                ('implementation_date', '<=', date(year, 12, 31))
            ])
            # Count events
            count += request.env['acara.post'].sudo().search_count([
                ('is_published', '=', True),
                ('event_date', '>=', date(year, 1, 1)),
                ('event_date', '<=', date(year, 12, 31))
            ])
            community_data.append(count)
        
        values['community_chart'] = {
            'labels': community_years,
            'data': community_data
        }
        
        # Reviewer chart data
        reviewer_years_found = []
        try:
            rev = request.env['reviewer.post'].sudo().search([('is_published', '=', True)], order='review_date asc', limit=1)
            if rev and rev.review_date:
                reviewer_years_found.append(rev.review_date.year)
        except:
            pass
        
        reviewer_years = get_years_for_category(min(reviewer_years_found) if reviewer_years_found else None)
        reviewer_data = []
        for year in reviewer_years:
            count = request.env['reviewer.post'].sudo().search_count([
                ('is_published', '=', True),
                ('review_date', '>=', date(year, 1, 1)),
                ('review_date', '<=', date(year, 12, 31))
            ])
            reviewer_data.append(count)
        
        values['reviewer_chart'] = {
            'labels': reviewer_years,
            'data': reviewer_data
        }
        
        return request.render('profile_dosen.profile_main_sinta', values)

    @http.route(['/profile/cv'], type='http', auth="public", website=True)
    def profile_cv(self, **kw):
        """Display CV page"""
        
        # Get the main profile
        post = request.env['profile.post'].sudo().search([
            ('is_published', '=', True),
            ('blog_id.is_main_profile', '=', True)
        ], limit=1)
        
        if not post:
            post = request.env['profile.post'].sudo().search([
                ('is_published', '=', True)
            ], order='sequence, id desc', limit=1)
        
        if not post:
            return request.not_found()
        
        # If CV not generated yet, generate it
        if not post.cv_document:
            cv_generator = request.env['cv.generator'].sudo().create({
                'profile_post_id': post.id,
            })
            cv_generator.generate_cv()
        
        # Get CV HTML
        if post.cv_document:
            import base64
            cv_html = base64.b64decode(post.cv_document).decode('utf-8')
        else:
            cv_html = "<p>CV belum tersedia</p>"
        
        values = {
            'post': post,
            'cv_html': cv_html,
        }
        
        return request.render('profile_dosen.profile_cv_view', values)

    @http.route(['/profile/download-cv'], type='http', auth="public", website=True)
    def profile_download_cv(self, **kw):
        """Download CV document"""

        # Get the main profile
        post = request.env['profile.post'].sudo().search([
            ('is_published', '=', True),
            ('blog_id.is_main_profile', '=', True)
        ], limit=1)
        
        if not post:
            post = request.env['profile.post'].sudo().search([
                ('is_published', '=', True)
            ], order='sequence, id desc', limit=1)

        if not post:
            return request.not_found()

        # Generate CV if not exists
        if not post.cv_document:
            try:
                cv_generator = request.env['cv.generator'].sudo().create({
                    'profile_post_id': post.id,
                })
                cv_generator.generate_cv()
                # Reload post to get updated cv_document
                post = request.env['profile.post'].sudo().browse(post.id)
            except Exception as e:
                # If generation fails, return error page
                return request.render('website.404', {'message': 'Gagal generate CV. Silakan coba lagi.'})

        if not post.cv_document:
            return request.render('website.404', {'message': 'CV belum tersedia. Silakan hubungi administrator.'})

        # Use Odoo's standard binary download URL
        download_url = f'/web/content/profile.post/{post.id}/cv_document?download=true'
        return request.redirect(download_url)
