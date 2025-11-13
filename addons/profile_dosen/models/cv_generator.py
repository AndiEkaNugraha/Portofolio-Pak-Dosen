# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
from datetime import datetime
import logging
import html as html_module
import re

_logger = logging.getLogger(__name__)


class CVGenerator(models.TransientModel):
    _name = 'cv.generator'
    _description = 'CV Generator'
    
    profile_post_id = fields.Many2one('profile.post', 'Profile', required=True)
    template_id = fields.Many2one('cv.template', 'Template CV', required=True)
    
    # Options
    include_photo = fields.Boolean('Sertakan Foto', default=True)
    language = fields.Selection([
        ('id', 'Bahasa Indonesia'),
        ('en', 'English'),
    ], string='Bahasa', default='id', required=True)
    
    # Generated CV
    cv_html = fields.Html('CV HTML', readonly=True)
    cv_file = fields.Binary('File CV', readonly=True, attachment=True)
    cv_filename = fields.Char('Nama File CV', readonly=True)
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        
        # Get profile_post_id from context
        profile_post_id = self.env.context.get('default_profile_post_id')
        if profile_post_id:
            profile = self.env['profile.post'].browse(profile_post_id)
            # Use profile's default template if set
            if profile.default_cv_template_id:
                res['template_id'] = profile.default_cv_template_id.id
                return res
        
        # Fallback: Set default template from cv.template
        default_template = self.env['cv.template'].get_default_template()
        if default_template:
            res['template_id'] = default_template.id
        return res
    
    def generate_cv(self):
        """Generate CV from all available data"""
        self.ensure_one()
        
        try:
            # Collect all data
            cv_data = self._collect_cv_data()
            
            # Generate HTML from template
            html_content = self._generate_html(cv_data)
            
            # Save HTML
            self.cv_html = html_content
            
            # Generate PDF using wkhtmltopdf
            pdf_content = self._generate_pdf(html_content)
            
            # Filename PDF
            filename = f"CV_{self.profile_post_id.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            
            # Update profile post with generated CV
            # CATATAN: CV disimpan sebagai file binary di cv_document, BUKAN di field content
            # Field content adalah untuk konten profil/biografi yang ditampilkan di website
            self.profile_post_id.write({
                'cv_document': pdf_content,
                'cv_document_filename': filename,
                'cv_generated_date': fields.Datetime.now(),
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('CV Berhasil Di-generate'),
                    'message': _('CV telah berhasil dibuat dan disimpan.'),
                    'type': 'success',
                    'sticky': False,
                    'next': {
                        'type': 'ir.actions.act_window_close',
                    },
                }
            }
            
        except Exception as e:
            _logger.error(f"Error generating CV: {str(e)}")
            raise UserError(_('Gagal membuat CV: %s') % str(e))
    
    def _collect_cv_data(self):
        """Collect all data from various modules"""
        self.ensure_one()
        profile = self.profile_post_id
        template = self.template_id
        
        data = {
            'profile': profile,
            'template': template,
            'generated_date': datetime.now(),
        }
        
        # Personal info & Biography
        if template.include_personal_info or template.include_biography:
            data['biography'] = {
                'name': profile.name,
                'subtitle': profile.subtitle,
                'content': profile.content,
                'teaser': profile.teaser,
                'photo': profile.cover_image if self.include_photo else False,
            }
        
        # Education
        if template.include_education:
            data['education'] = profile.education_ids.filtered(lambda e: e.active).sorted(
                key=lambda e: (e.end_year or 9999, e.start_year), 
                reverse=template.sort_descending
            )
        
        # Work Experience
        if template.include_work_experience:
            data['work_experience'] = profile.work_ids.filtered(lambda w: w.active).sorted(
                key=lambda w: (w.end_date or fields.Date.today(), w.start_date),
                reverse=template.sort_descending
            )
        
        # Expertise
        if template.include_expertise:
            data['expertise'] = profile.expertise_ids.filtered(lambda e: e.active).sorted(
                key=lambda e: e.sequence
            )
        
        # Awards
        if template.include_awards:
            data['awards'] = profile.award_ids.filtered(lambda a: a.active).sorted(
                key=lambda a: a.award_date,
                reverse=template.sort_descending
            )
        
        # Publications (from jurnal_ilmiah)
        if template.include_publications:
            try:
                publications = self.env['jurnal.post'].search([
                    ('is_published', '=', True)
                ], order='publication_year desc' if template.sort_descending else 'publication_year asc')
                
                if template.limit_publications > 0:
                    publications = publications[:template.limit_publications]
                    
                data['publications'] = publications
            except Exception as e:
                _logger.warning(f"Could not load publications: {str(e)}")
                data['publications'] = []
        
        # Books (from buku_karya)
        if template.include_books:
            try:
                books = self.env['buku.post'].search([
                    ('is_published', '=', True)
                ], order='publication_year desc' if template.sort_descending else 'publication_year asc')
                data['books'] = books
            except Exception as e:
                _logger.warning(f"Could not load books: {str(e)}")
                data['books'] = []
        
        # Patents (from hki_paten)
        if template.include_patents:
            try:
                patents = self.env['hki.post'].search([
                    ('is_published', '=', True)
                ], order='registration_date desc' if template.sort_descending else 'registration_date asc')
                data['patents'] = patents
            except Exception as e:
                _logger.warning(f"Could not load patents: {str(e)}")
                data['patents'] = []
        
        # Research Projects (from proyek_penelitian)
        if template.include_research_projects:
            try:
                projects = self.env['proyek.penelitian.post'].search([
                    ('is_published', '=', True)
                ], order='start_date desc' if template.sort_descending else 'start_date asc')
                
                if template.limit_projects > 0:
                    projects = projects[:template.limit_projects]
                
                _logger.info(f"Found {len(projects)} research projects")
                data['research_projects'] = projects
            except Exception as e:
                _logger.warning(f"Could not load research projects: {str(e)}")
                data['research_projects'] = []
        
        # Community Service (from pengabdian_masyarakat)
        if template.include_community_service:
            try:
                community_service = self.env['pengabdian.post'].search([
                    ('is_published', '=', True)
                ], order='implementation_date desc' if template.sort_descending else 'implementation_date asc')
                _logger.info(f"Found {len(community_service)} community service activities")
                data['community_service'] = community_service
            except Exception as e:
                _logger.warning(f"Could not load community service: {str(e)}")
                data['community_service'] = []
        
        # Conferences (from prosiding_konferensi)
        if template.include_conferences:
            try:
                conferences = self.env['prosiding.post'].search([
                    ('is_published', '=', True)
                ], order='conference_date desc' if template.sort_descending else 'conference_date asc')
                data['conferences'] = conferences
            except Exception as e:
                _logger.warning(f"Could not load conferences: {str(e)}")
                data['conferences'] = []
        
        # Grants (from hibah_pendanaan)
        if template.include_grants:
            try:
                # hibah_pendanaan menggunakan website_published, bukan is_published
                grants = self.env['hibah.pendanaan.post'].search([
                    ('website_published', '=', True)
                ], order='start_date desc' if template.sort_descending else 'start_date asc')
                _logger.info(f"Found {len(grants)} grants")
                data['grants'] = grants
            except Exception as e:
                _logger.warning(f"Could not load grants: {str(e)}")
                data['grants'] = []
        
        # Research Products (from produk_penelitian)
        if template.include_research_products:
            try:
                products = self.env['produk.post'].search([
                    ('is_published', '=', True)
                ], order='development_date desc' if template.sort_descending else 'development_date asc')
                _logger.info(f"Found {len(products)} research products")
                data['research_products'] = products
            except Exception as e:
                _logger.warning(f"Could not load research products: {str(e)}")
                data['research_products'] = []
        
        # Reviewer Activities (from reviewer_dosen)
        if template.include_reviewer_activities:
            try:
                reviewer_activities = self.env['reviewer.post'].search([
                    ('is_published', '=', True)
                ], order='review_date desc' if template.sort_descending else 'review_date asc')
                data['reviewer_activities'] = reviewer_activities
            except Exception as e:
                _logger.warning(f"Could not load reviewer activities: {str(e)}")
                data['reviewer_activities'] = []
        
        # Events (from acara_dosen)
        if template.include_events:
            try:
                # acara_dosen hanya punya field active, tidak ada is_published
                events = self.env['acara.post'].search([
                    ('active', '=', True)
                ], order='event_date desc' if template.sort_descending else 'event_date asc')
                _logger.info(f"Found {len(events)} events")
                data['events'] = events
            except Exception as e:
                _logger.warning(f"Could not load events: {str(e)}")
                data['events'] = []
        
        # Research Groups (from grup_riset)
        if template.include_research_groups:
            try:
                research_groups = self.env['grup.riset.post'].search([
                    ('is_published', '=', True)
                ])
                _logger.info(f"Found {len(research_groups)} research groups")
                data['research_groups'] = research_groups
            except Exception as e:
                _logger.warning(f"Could not load research groups: {str(e)}")
                data['research_groups'] = []
        
        # Courses (from mata_kuliah)
        if template.include_courses:
            try:
                courses = self.env['matakuliah.post'].search([
                    ('is_published', '=', True)
                ])
                data['courses'] = courses
            except Exception as e:
                _logger.warning(f"Could not load courses: {str(e)}")
                data['courses'] = []
        
        return data
    
    def _generate_html(self, cv_data):
        """Generate HTML from template and data"""
        self.ensure_one()
        
        # Debug: Check if template has custom HTML
        _logger.info(f"=== CV Generator Debug ===")
        _logger.info(f"Template ID: {self.template_id.id}")
        _logger.info(f"Template Name: {self.template_id.name}")
        _logger.info(f"Has custom_html_template: {bool(self.template_id.custom_html_template)}")
        if self.template_id.custom_html_template:
            _logger.info(f"Template length: {len(self.template_id.custom_html_template)} chars")
        
        # Use custom HTML template if available
        if self.template_id.custom_html_template:
            try:
                html = self._render_custom_html(cv_data)
                _logger.info(f"Successfully rendered custom HTML template ({len(html)} chars)")
                return html
            except Exception as e:
                _logger.error(f"ERROR rendering custom HTML template: {str(e)}", exc_info=True)
                raise UserError(f"Gagal render template CV: {str(e)}")
        
        # Fallback: Generate basic HTML
        _logger.warning("No custom HTML template found, using basic HTML fallback")
        return self._generate_basic_html(cv_data)
    
    def _escape_html(self, text):
        """Escape HTML special characters untuk plain text"""
        if not text:
            return ''
        # Escape HTML special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text
    
    def _clean_html_field(self, html_text):
        """Clean HTML field content - remove outer html/body tags but keep inner content"""
        if not html_text:
            return ''
        # Remove outer html/body/head tags if present
        html_text = re.sub(r'</?html[^>]*>', '', html_text, flags=re.IGNORECASE)
        html_text = re.sub(r'</?body[^>]*>', '', html_text, flags=re.IGNORECASE)
        html_text = re.sub(r'<head>.*?</head>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
        return html_text.strip()
    
    def _render_custom_html(self, cv_data):
        """Render custom HTML template dengan placeholder substitution"""
        profile = cv_data['profile']
        template = cv_data['template']
        
        # Get template HTML
        html_template = template.custom_html_template
        if not html_template:
            raise ValueError("Template HTML kosong")
        
        _logger.info(f"Rendering custom HTML for profile: {profile.name}")
        _logger.info(f"Template HTML length: {len(html_template)} chars")
        
        # Prepare placeholder values
        # IMPORTANT: Clean HTML content to prevent nested HTML structure issues
        biography_content = profile.content or profile.teaser or ''
        # Remove outer html/body/head tags if present in content field
        biography_content = re.sub(r'</?html[^>]*>', '', biography_content, flags=re.IGNORECASE)
        biography_content = re.sub(r'</?body[^>]*>', '', biography_content, flags=re.IGNORECASE)
        biography_content = re.sub(r'<head>.*?</head>', '', biography_content, flags=re.DOTALL | re.IGNORECASE)
        
        placeholders = {
            'profile_name': self._escape_html(profile.name or ''),
            'profile_subtitle': self._escape_html(profile.subtitle or ''),
            'profile_biography': biography_content,  # Keep inner HTML tags like <h2>, <p>, etc
            'custom_css': template.custom_css or '',
        }
        
        # Generate HTML for each section
        if cv_data.get('education'):
            education_html = ''
            for edu in cv_data['education']:
                period = f"{edu.start_year} - {edu.end_year or 'Sekarang'}"
                education_html += f"""
                <div class="education-item">
                    <h4>{self._escape_html(edu.degree.upper())} - {self._escape_html(edu.major)}</h4>
                    <p class="institution">{self._escape_html(edu.institution)}</p>
                    <p class="period">{period}</p>
                    {f'<p class="gpa">GPA: {edu.gpa}</p>' if edu.gpa else ''}
                </div>
                """
            placeholders['education_html'] = education_html
        else:
            placeholders['education_html'] = ''
        
        if cv_data.get('work_experience'):
            work_html = ''
            for work in cv_data['work_experience']:
                period = f"{work.start_date.strftime('%B %Y') if work.start_date else ''} - {work.end_date.strftime('%B %Y') if work.end_date else 'Sekarang'}"
                # Clean description HTML to prevent nested issues
                description = self._clean_html_field(work.description) if work.description else ''
                work_html += f"""
                <div class="work-item">
                    <h4>{self._escape_html(work.position)}</h4>
                    <p class="institution">{self._escape_html(work.institution)}</p>
                    <p class="period">{period}</p>
                    {f'<p class="description">{description}</p>' if description else ''}
                </div>
                """
            placeholders['work_experience_html'] = work_html
        else:
            placeholders['work_experience_html'] = ''
        
        if cv_data.get('expertise'):
            expertise_html = '<ul class="expertise-list">'
            for exp in cv_data['expertise']:
                expertise_html += f'<li><strong>{self._escape_html(exp.name)}</strong> - {self._escape_html(exp.expertise_type)}</li>'
            expertise_html += '</ul>'
            placeholders['expertise_html'] = expertise_html
        else:
            placeholders['expertise_html'] = ''
        
        if cv_data.get('awards'):
            awards_html = ''
            for award in cv_data['awards']:
                awards_html += f"""
                <div class="award-item">
                    <h4>{self._escape_html(award.name)}</h4>
                    <p class="organization">{self._escape_html(award.issuer)}</p>
                    <p class="date">{award.award_date.strftime('%B %Y') if award.award_date else ''}</p>
                </div>
                """
            placeholders['awards_html'] = awards_html
        else:
            placeholders['awards_html'] = ''
        
        # Get base URL for links
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        
        # Publications (Jurnal Ilmiah)
        if cv_data.get('publications'):
            publications_html = ''
            for pub in cv_data['publications']:
                authors = self._escape_html(pub.authors if hasattr(pub, 'authors') else profile.name)
                journal = self._escape_html(pub.journal_name if hasattr(pub, 'journal_name') else '')
                year = pub.publication_year if hasattr(pub, 'publication_year') else ''
                # Get URL slug - judul langsung clickable
                pub_url = f"{base_url}/jurnal-ilmiah/{pub.slug}" if hasattr(pub, 'slug') and pub.slug else ''
                if pub_url:
                    title_html = f'<a href="{self._escape_html(pub_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(pub.name)}</a>'
                else:
                    title_html = self._escape_html(pub.name)
                # Clean teaser HTML
                teaser = self._clean_html_field(pub.teaser) if hasattr(pub, 'teaser') and pub.teaser else ''
                publications_html += f"""
                <div class="publication-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="publication-meta">{authors}. <em>{journal}</em>, {year}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['publications_html'] = publications_html
        else:
            placeholders['publications_html'] = ''
        
        # Books (Buku Karya)
        if cv_data.get('books'):
            books_html = ''
            for book in cv_data['books']:
                publisher = self._escape_html(book.publisher_name if hasattr(book, 'publisher_name') else '')
                year = book.publication_year if hasattr(book, 'publication_year') else ''
                book_url = f"{base_url}/buku-karya/{book.slug}" if hasattr(book, 'slug') and book.slug else ''
                if book_url:
                    title_html = f'<a href="{self._escape_html(book_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(book.name)}</a>'
                else:
                    title_html = self._escape_html(book.name)
                teaser = self._clean_html_field(book.teaser) if hasattr(book, 'teaser') and book.teaser else ''
                books_html += f"""
                <div class="book-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="book-meta">{publisher}, {year}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['books_html'] = books_html
        else:
            placeholders['books_html'] = ''
        
        # Patents (HKI/Paten)
        if cv_data.get('patents'):
            patents_html = ''
            for patent in cv_data['patents']:
                cert_number = self._escape_html(patent.certificate_number if hasattr(patent, 'certificate_number') else '')
                reg_date = patent.registration_date.strftime('%Y') if hasattr(patent, 'registration_date') and patent.registration_date else ''
                patent_url = f"{base_url}/hki-paten/{patent.slug}" if hasattr(patent, 'slug') and patent.slug else ''
                if patent_url:
                    title_html = f'<a href="{self._escape_html(patent_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(patent.name)}</a>'
                else:
                    title_html = self._escape_html(patent.name)
                teaser = self._clean_html_field(patent.teaser) if hasattr(patent, 'teaser') and patent.teaser else ''
                patents_html += f"""
                <div class="patent-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="patent-meta">Certificate: {cert_number} | Registration: {reg_date}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['patents_html'] = patents_html
        else:
            placeholders['patents_html'] = ''
        
        # Research Projects (Proyek Penelitian)
        if cv_data.get('research_projects'):
            projects_html = ''
            _logger.info(f"Rendering {len(cv_data['research_projects'])} research projects to HTML")
            for project in cv_data['research_projects']:
                start_year = project.start_date.year if hasattr(project, 'start_date') and project.start_date else ''
                end_year = project.end_date.year if hasattr(project, 'end_date') and project.end_date else 'Present'
                project_url = f"{base_url}/proyek-penelitian/{project.slug}" if hasattr(project, 'slug') and project.slug else ''
                if project_url:
                    title_html = f'<a href="{self._escape_html(project_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(project.name)}</a>'
                else:
                    title_html = self._escape_html(project.name)
                teaser = self._clean_html_field(project.teaser) if hasattr(project, 'teaser') and project.teaser else ''
                projects_html += f"""
                <div class="project-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="project-meta">{start_year} - {end_year}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['projects_html'] = projects_html
            _logger.info(f"Generated projects_html length: {len(projects_html)} chars")
        else:
            _logger.warning("No research_projects data found in cv_data")
            placeholders['projects_html'] = ''
        
        # Community Service (Pengabdian Masyarakat)
        if cv_data.get('community_service'):
            community_html = ''
            for service in cv_data['community_service']:
                impl_year = service.implementation_date.year if hasattr(service, 'implementation_date') and service.implementation_date else ''
                service_url = f"{base_url}/pengabdian-masyarakat/{service.slug}" if hasattr(service, 'slug') and service.slug else ''
                if service_url:
                    title_html = f'<a href="{self._escape_html(service_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(service.name)}</a>'
                else:
                    title_html = self._escape_html(service.name)
                teaser = self._clean_html_field(service.teaser) if hasattr(service, 'teaser') and service.teaser else ''
                community_html += f"""
                <div class="community-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="community-meta">{impl_year}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['community_service_html'] = community_html
        else:
            placeholders['community_service_html'] = ''
        
        # Conferences (Prosiding Konferensi)
        if cv_data.get('conferences'):
            conferences_html = ''
            for conf in cv_data['conferences']:
                conf_name = self._escape_html(conf.conference_name if hasattr(conf, 'conference_name') else '')
                conf_date = conf.conference_date.strftime('%Y') if hasattr(conf, 'conference_date') and conf.conference_date else ''
                conf_url = f"{base_url}/prosiding-konferensi/{conf.slug}" if hasattr(conf, 'slug') and conf.slug else ''
                if conf_url:
                    title_html = f'<a href="{self._escape_html(conf_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(conf.name)}</a>'
                else:
                    title_html = self._escape_html(conf.name)
                teaser = self._clean_html_field(conf.teaser) if hasattr(conf, 'teaser') and conf.teaser else ''
                conferences_html += f"""
                <div class="conference-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="conference-meta">{conf_name}, {conf_date}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['conferences_html'] = conferences_html
        else:
            placeholders['conferences_html'] = ''
        
        # Grants (Hibah Pendanaan)
        if cv_data.get('grants'):
            grants_html = ''
            for grant in cv_data['grants']:
                funding_source = self._escape_html(grant.funding_source if hasattr(grant, 'funding_source') else '')
                start_year = grant.start_date.year if hasattr(grant, 'start_date') and grant.start_date else ''
                grant_url = f"{base_url}/hibah-pendanaan/{grant.slug}" if hasattr(grant, 'slug') and grant.slug else ''
                if grant_url:
                    title_html = f'<a href="{self._escape_html(grant_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(grant.name)}</a>'
                else:
                    title_html = self._escape_html(grant.name)
                teaser = self._clean_html_field(grant.teaser) if hasattr(grant, 'teaser') and grant.teaser else ''
                grants_html += f"""
                <div class="grant-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="grant-meta">{funding_source}, {start_year}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['grants_html'] = grants_html
        else:
            placeholders['grants_html'] = ''
        
        # Research Products (Produk Penelitian)
        if cv_data.get('research_products'):
            products_html = ''
            for product in cv_data['research_products']:
                dev_year = product.development_date.year if hasattr(product, 'development_date') and product.development_date else ''
                product_url = f"{base_url}/produk-penelitian/{product.slug}" if hasattr(product, 'slug') and product.slug else ''
                if product_url:
                    title_html = f'<a href="{self._escape_html(product_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(product.name)}</a>'
                else:
                    title_html = self._escape_html(product.name)
                teaser = self._clean_html_field(product.teaser) if hasattr(product, 'teaser') and product.teaser else ''
                products_html += f"""
                <div class="product-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="product-meta">Year: {dev_year}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['products_html'] = products_html
        else:
            placeholders['products_html'] = ''
        
        # Reviewer Activities
        if cv_data.get('reviewer_activities'):
            reviewer_html = ''
            for review in cv_data['reviewer_activities']:
                journal = self._escape_html(review.journal_conference_name if hasattr(review, 'journal_conference_name') else '')
                review_date = review.review_date.strftime('%Y') if hasattr(review, 'review_date') and review.review_date else ''
                review_url = f"{base_url}/reviewer-dosen/{review.slug}" if hasattr(review, 'slug') and review.slug else ''
                if review_url:
                    title_html = f'<a href="{self._escape_html(review_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(review.name)}</a>'
                else:
                    title_html = self._escape_html(review.name)
                reviewer_html += f"""
                <div class="reviewer-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="reviewer-meta">{journal}, {review_date}</p>
                </div>
                """
            placeholders['reviewer_html'] = reviewer_html
        else:
            placeholders['reviewer_html'] = ''
        
        # Events (Acara Dosen)
        if cv_data.get('events'):
            events_html = ''
            for event in cv_data['events']:
                event_date = event.event_date.strftime('%Y') if hasattr(event, 'event_date') and event.event_date else ''
                event_url = f"{base_url}/acara-dosen/{event.slug}" if hasattr(event, 'slug') and event.slug else ''
                if event_url:
                    title_html = f'<a href="{self._escape_html(event_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(event.name)}</a>'
                else:
                    title_html = self._escape_html(event.name)
                teaser = self._clean_html_field(event.teaser) if hasattr(event, 'teaser') and event.teaser else ''
                events_html += f"""
                <div class="event-item">
                    <p><strong>{title_html}</strong></p>
                    <p class="event-meta">{event_date}</p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['events_html'] = events_html
        else:
            placeholders['events_html'] = ''
        
        # Research Groups
        if cv_data.get('research_groups'):
            groups_html = ''
            for group in cv_data['research_groups']:
                group_url = f"{base_url}/grup-riset/{group.slug}" if hasattr(group, 'slug') and group.slug else ''
                if group_url:
                    title_html = f'<a href="{self._escape_html(group_url)}" style="color: #2c3e50; text-decoration: none;">{self._escape_html(group.name)}</a>'
                else:
                    title_html = self._escape_html(group.name)
                teaser = self._clean_html_field(group.teaser) if hasattr(group, 'teaser') and group.teaser else ''
                groups_html += f"""
                <div class="group-item">
                    <p><strong>{title_html}</strong></p>
                    {f'<p class="description">{teaser}</p>' if teaser else ''}
                </div>
                """
            placeholders['groups_html'] = groups_html
        else:
            placeholders['groups_html'] = ''
        
        # Replace placeholders in template
        html = html_template
        for key, value in placeholders.items():
            html = html.replace(f'${{{key}}}', str(value))
        
        # Auto-wrap jika template tidak lengkap (tidak ada <!DOCTYPE html>)
        if not html.strip().startswith('<!DOCTYPE') and not html.strip().startswith('<html'):
            _logger.info("Template HTML tidak lengkap, melakukan auto-wrap dengan HTML structure")
            html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Curriculum Vitae - {profile.name}</title>
    <style>
{template.custom_css or ''}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        
        return html
    
    def _generate_basic_html(self, cv_data):
        """Generate basic HTML CV (fallback)"""
        profile = cv_data['profile']
        template = cv_data['template']
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>CV - {profile.name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 2px solid #95a5a6;
                    padding-bottom: 5px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #555;
                    margin-bottom: 5px;
                }}
                .section {{
                    margin-bottom: 30px;
                }}
                .item {{
                    margin-bottom: 20px;
                    padding-left: 20px;
                }}
                .date {{
                    color: #7f8c8d;
                    font-style: italic;
                }}
                .organization {{
                    color: #2980b9;
                    font-weight: bold;
                }}
                {template.custom_css or ''}
            </style>
        </head>
        <body>
            <h1>{profile.name}</h1>
        """
        
        if profile.subtitle:
            html += f"<p><strong>{profile.subtitle}</strong></p>"
        
        # Biography
        if template.include_biography and cv_data.get('biography'):
            html += """
            <div class="section">
                <h2>Biografi</h2>
            """
            if profile.teaser:
                html += f"<p>{profile.teaser}</p>"
            html += "</div>"
        
        # Education
        if template.include_education and cv_data.get('education'):
            html += """
            <div class="section">
                <h2>Pendidikan</h2>
            """
            for edu in cv_data['education']:
                period = f"{edu.start_year} - {edu.end_year or 'Sekarang'}"
                html += f"""
                <div class="item">
                    <h3>{edu.degree.upper()} - {edu.major}</h3>
                    <p class="organization">{edu.institution}</p>
                    <p class="date">{period}</p>
                </div>
                """
            html += "</div>"
        
        # Work Experience
        if template.include_work_experience and cv_data.get('work_experience'):
            html += """
            <div class="section">
                <h2>Pengalaman Kerja</h2>
            """
            for work in cv_data['work_experience']:
                period = f"{work.start_date.strftime('%Y-%m') if work.start_date else ''} - {work.end_date.strftime('%Y-%m') if work.end_date else 'Sekarang'}"
                html += f"""
                <div class="item">
                    <h3>{work.position}</h3>
                    <p class="organization">{work.institution}</p>
                    <p class="date">{period}</p>
                </div>
                """
            html += "</div>"
        
        # Add other sections similarly...
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def _sanitize_html_for_pdf(self, html_content):
        """Sanitize HTML untuk membuat kompatibel dengan wkhtmltopdf"""
        import re
        
        # Ensure we're working with string, not bytes
        if isinstance(html_content, bytes):
            html = html_content.decode('utf-8', errors='replace')
        else:
            html = html_content
        
        # Remove BOM if present
        if html.startswith('\ufeff'):
            html = html[1:]
            _logger.info("Removed BOM from HTML")
        
        # Replace problematic DOCTYPE dengan yang sederhana
        html = re.sub(r'<!DOCTYPE[^>]*>', '<!DOCTYPE html>', html, flags=re.IGNORECASE)
        
        # Ensure DOCTYPE exists at the start
        if not html.strip().startswith('<!DOCTYPE'):
            html = '<!DOCTYPE html>\n' + html
            _logger.info("Added DOCTYPE to HTML")
        
        # Ensure proper HTML structure
        if not re.search(r'<html[^>]*>', html, re.IGNORECASE):
            html = html.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<html lang="id">')
            if '</html>' not in html.lower():
                html += '\n</html>'
            _logger.info("Added HTML tags")
        
        # Ensure head section exists
        if not re.search(r'<head[^>]*>', html, re.IGNORECASE):
            html = html.replace('<html', '<html>\n<head>\n<meta charset="UTF-8">\n<title>CV</title>\n</head>', 1)
            _logger.info("Added HEAD section")
        
        # Ensure charset UTF-8 in meta tag (wkhtmltopdf requires this as FIRST element in head)
        if '<head>' in html or '<head ' in html:
            head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL | re.IGNORECASE)
            if head_match:
                head_content = head_match.group(1)
                # Remove existing charset meta tag
                head_content_clean = re.sub(r'<meta[^>]*charset[^>]*>', '', head_content, flags=re.IGNORECASE)
                # Add charset as FIRST element
                new_head_content = '\n    <meta charset="UTF-8">' + head_content_clean
                html = html[:head_match.start(1)] + new_head_content + html[head_match.end(1):]
                _logger.info("Fixed charset meta tag position")
        
        # Ensure body section exists
        if not re.search(r'<body[^>]*>', html, re.IGNORECASE):
            html = html.replace('</head>', '</head>\n<body>')
            if '</body>' not in html.lower():
                html = html.replace('</html>', '</body>\n</html>')
            _logger.info("Added BODY tags")
        
        # Remove any HTML comments that might confuse wkhtmltopdf
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # Fix nested HTML content dalam field content (avoid double <html>)
        # Cek jika ada <html> dalam <body>
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
        if body_match:
            body_content = body_match.group(1)
            if '<html' in body_content.lower():
                _logger.warning("Detected nested HTML in body content - cleaning up")
                # Remove nested html/head/body tags
                body_content = re.sub(r'</?html[^>]*>', '', body_content, flags=re.IGNORECASE)
                body_content = re.sub(r'<head>.*?</head>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                body_content = re.sub(r'</?body[^>]*>', '', body_content, flags=re.IGNORECASE)
                html = html[:body_match.start(1)] + body_content + html[body_match.end(1):]
        
        # Decode HTML entities CAREFULLY - only once to prevent double-decoding
        # IMPORTANT: Jangan decode entities dalam tag HTML
        try:
            # Unescape HTML entities dalam text content, tapi preserve entities dalam attributes
            # Simplified approach: only unescape common problematic entities
            html = html.replace('&amp;nbsp;', '&nbsp;')
            html = html.replace('&amp;#', '&#')
            html = html.replace('&amp;lt;', '&lt;')
            html = html.replace('&amp;gt;', '&gt;')
            html = html.replace('&amp;quot;', '&quot;')
        except Exception as e:
            _logger.warning(f"Could not process HTML entities: {e}")
        
        # Replace problematic Unicode characters yang tidak render baik di PDF
        replacements = {
            '\u00a0': ' ',   # Non-breaking space -> space
            '\u200b': '',    # Zero-width space -> hapus
            '\u200c': '',    # Zero-width non-joiner -> hapus
            '\u200d': '',    # Zero-width joiner -> hapus
            '\ufeff': '',    # Zero-width no-break space (BOM) -> hapus
            '\u2013': '-',   # En dash -> hyphen
            '\u2014': '-',   # Em dash -> hyphen
            '\u2018': "'",   # Left single quote -> straight quote
            '\u2019': "'",   # Right single quote -> straight quote
            '\u201a': "'",   # Single low quote -> straight quote
            '\u201b': "'",   # Single high-reversed quote -> straight quote
            '\u201c': '"',   # Left double quote -> straight quote
            '\u201d': '"',   # Right double quote -> straight quote
            '\u201e': '"',   # Double low quote -> straight quote
            '\u201f': '"',   # Double high-reversed quote -> straight quote
            '\u2022': '*',   # Bullet -> asterisk
            '\u2026': '...', # Ellipsis -> three dots
        }
        for old, new in replacements.items():
            html = html.replace(old, new)
        
        # Ensure proper closing tags
        if '</html>' not in html.lower():
            html += '\n</html>'
        if '</body>' not in html.lower() and '<body' in html.lower():
            html = html.replace('</html>', '</body>\n</html>')
        
        # Fix common HTML issues
        # Remove multiple consecutive newlines (keep max 2)
        html = re.sub(r'\n{3,}', '\n\n', html)
        
        # Fix malformed tags (tags with spaces before >)
        html = re.sub(r'\s+>', '>', html)
        
        # Remove completely empty elements that cause spacing issues
        html = re.sub(r'<p[^>]*>\s*</p>', '', html)
        html = re.sub(r'<div[^>]*>\s*</div>', '', html)
        html = re.sub(r'<span[^>]*>\s*</span>', '', html)
        
        # Validate basic HTML structure
        if html.count('<html') != html.count('</html>'):
            _logger.error("HTML tag mismatch detected!")
        if html.count('<head') != html.count('</head>'):
            _logger.error("HEAD tag mismatch detected!")
        if html.count('<body') != html.count('</body>'):
            _logger.error("BODY tag mismatch detected!")
        
        _logger.info(f"HTML sanitized successfully, final size: {len(html)} bytes")
        
        return html
    
    def _generate_pdf(self, html_content):
        """Generate PDF from HTML using wkhtmltopdf with improved error handling"""
        try:
            # Sanitize HTML untuk wkhtmltopdf
            html_for_pdf = self._sanitize_html_for_pdf(html_content)
            
            _logger.info(f"Starting PDF generation, HTML size: {len(html_for_pdf)} bytes")
            _logger.info(f"HTML type: {type(html_for_pdf)}")
            
            # Menggunakan IrActionsReport untuk generate PDF
            IrActionsReport = self.env['ir.actions.report']
            
            # IMPORTANT: Odoo's _run_wkhtmltopdf expects STRING, not bytes
            # It will do the encoding internally (see ir_actions_report.py line 600)
            if isinstance(html_for_pdf, bytes):
                _logger.info("Converting bytes back to string for Odoo")
                html_string = html_for_pdf.decode('utf-8', errors='replace')
            else:
                _logger.info("Using HTML string directly")
                html_string = html_for_pdf
            
            _logger.info(f"HTML string size: {len(html_string)} characters")
            
            # Prepare wkhtmltopdf options dengan margin yang konsisten
            # IMPORTANT: Set margin yang seimbang untuk semua sisi
            # Margin bawah sedikit lebih besar untuk tampilan yang lebih baik
            specific_paperformat_args = {
                'data-report-margin-top': 15,      # 15mm margin atas
                'data-report-margin-bottom': 15,   # 15mm margin bawah
                'data-report-margin-left': 15,     # 15mm margin kiri
                'data-report-margin-right': 15,    # 15mm margin kanan
                'data-report-header-spacing': 0,   # Tidak ada spacing untuk header
                'data-report-dpi': 96,             # DPI standar untuk screen/print
            }
            
            # Call wkhtmltopdf - gunakan method yang BENAR
            # _run_wkhtmltopdf expects: (bodies, report_ref=False, header=None, footer=None, 
            #                            landscape=False, specific_paperformat_args=None, set_viewport_size=False)
            # IMPORTANT: bodies must be list of STRINGS, not bytes (Odoo will encode internally)
            try:
                pdf_result = IrActionsReport._run_wkhtmltopdf(
                    bodies=[html_string],
                    report_ref=False,
                    header=None,
                    footer=None,
                    landscape=False,
                    specific_paperformat_args=specific_paperformat_args,
                    set_viewport_size=False
                )
                # Handle result - bisa berupa bytes atau tuple (bytes, content_type)
                if isinstance(pdf_result, tuple):
                    pdf_content = pdf_result[0]
                    content_type = pdf_result[1] if len(pdf_result) > 1 else 'application/pdf'
                    _logger.info(f"PDF generated with content_type: {content_type}")
                else:
                    pdf_content = pdf_result
                    _logger.info("PDF generated successfully")
                    
            except TypeError as te:
                # Jika signature method berbeda di versi Odoo ini
                _logger.warning(f"TypeError calling _run_wkhtmltopdf: {te}, trying alternative signature...")
                try:
                    # Try simpler call
                    pdf_result = IrActionsReport._run_wkhtmltopdf(
                        [html_string],
                        landscape=False,
                        specific_paperformat_args=specific_paperformat_args
                    )
                    if isinstance(pdf_result, tuple):
                        pdf_content = pdf_result[0]
                    else:
                        pdf_content = pdf_result
                except Exception as e2:
                    _logger.error(f"Alternative call also failed: {e2}")
                    # Last resort: simplest possible call
                    pdf_result = IrActionsReport._run_wkhtmltopdf([html_string])
                    if isinstance(pdf_result, tuple):
                        pdf_content = pdf_result[0]
                    else:
                        pdf_content = pdf_result
            
            # Validasi PDF content
            if not pdf_content:
                raise ValueError("PDF content is empty after wkhtmltopdf execution")
            
            if len(pdf_content) < 100:
                raise ValueError(f"PDF content too small: {len(pdf_content)} bytes - likely corrupted")
            
            # Check PDF magic number (PDF files MUST start with %PDF)
            if not pdf_content.startswith(b'%PDF'):
                # Log first 200 bytes untuk debugging
                preview = pdf_content[:200]
                _logger.error(f"Invalid PDF header detected!")
                _logger.error(f"First 200 bytes (hex): {preview.hex()}")
                _logger.error(f"First 200 bytes (repr): {repr(preview)}")
                
                # Try to detect what we got instead
                if pdf_content.startswith(b'<'):
                    raise ValueError("Generated content is HTML, not PDF - wkhtmltopdf failed to convert")
                elif pdf_content.startswith(b'\x00'):
                    raise ValueError("Generated content contains null bytes - encoding issue")
                else:
                    raise ValueError(f"Generated content is not a valid PDF file (header: {preview[:20]})")
            
            _logger.info(f"✓ PDF generated successfully, size: {len(pdf_content)} bytes")
            _logger.info(f"✓ PDF header verified: {pdf_content[:20]}")
            
            # Encode to base64 untuk disimpan di database
            return base64.b64encode(pdf_content)
            
        except Exception as e:
            _logger.error(f"✗ Failed to generate PDF: {str(e)}")
            _logger.error(f"Error type: {type(e).__name__}")
            import traceback
            _logger.error(f"Traceback:\n{traceback.format_exc()}")
            
            # Log HTML untuk debugging (first 1000 chars)
            _logger.debug(f"HTML content (first 1000 chars):\n{html_content[:1000]}")
            
            # Don't fallback to HTML - raise error instead
            # Ini lebih baik karena user tahu ada masalah daripada dapat file corrupt
            raise UserError(_(
                'Gagal generate PDF: %s\n\n'
                'Kemungkinan penyebab:\n'
                '1. wkhtmltopdf tidak terinstall atau tidak berfungsi\n'
                '2. HTML template mengandung syntax error\n'
                '3. Konten HTML terlalu kompleks\n\n'
                'Silakan cek log server untuk detail lebih lanjut.'
            ) % str(e))
    
    def action_test_pdf(self):
        """Test PDF generation dengan HTML sederhana"""
        try:
            # Test dengan HTML sangat sederhana
            test_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Test PDF</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    h1 { color: #333; }
                </style>
            </head>
            <body>
                <h1>Test PDF Generation</h1>
                <p>Jika Anda bisa membaca ini dalam PDF, maka wkhtmltopdf berfungsi dengan baik.</p>
                <p>Test Date: """ + str(datetime.now()) + """</p>
            </body>
            </html>
            """
            
            IrActionsReport = self.env['ir.actions.report']
            html_bytes = test_html.encode('utf-8')
            
            _logger.info("Testing PDF generation with simple HTML...")
            pdf_content = IrActionsReport._run_wkhtmltopdf(
                [html_bytes],
                landscape=False
            )
            
            if isinstance(pdf_content, tuple):
                pdf_content = pdf_content[0]
            
            _logger.info(f"Test PDF generated: {len(pdf_content)} bytes")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Test Berhasil'),
                    'message': _('PDF generation test successful! Size: %d bytes') % len(pdf_content),
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            _logger.error(f"Test failed: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Test Gagal'),
                    'message': _('PDF generation test failed: %s') % str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }
    
    def action_preview_cv(self):
        """Preview generated CV"""
        self.generate_cv()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Preview CV',
            'res_model': 'cv.generator',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def action_download_cv(self):
        """Download generated CV"""
        if not self.profile_post_id.cv_document:
            self.generate_cv()
        
        return self.profile_post_id.action_download_cv()
