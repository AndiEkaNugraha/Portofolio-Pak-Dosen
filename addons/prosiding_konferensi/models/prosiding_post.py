# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ProsidingPost(models.Model):
    _name = 'prosiding.post'
    _inherit = 'blog.post'
    _description = 'Entri Prosiding Konferensi'
    
    # Override fields dari blog post
    name = fields.Char('Judul Paper', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul atau judul kecil")
    blog_id = fields.Many2one('prosiding.blog', 'Kategori Konferensi', required=True, ondelete='cascade')
    
    # Field inherited dari blog.post: create_date, write_date, active, website_published, publication_date
    
    # SEO fields
    slug = fields.Char('URL Slug', compute='_compute_slug', store=True, inverse='_inverse_slug', index=True)
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan judul paper jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan sinopsis jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
        
    # Override blog fields dengan label yang jelas untuk prosiding
    teaser = fields.Char('Sinopsis', help="Ringkasan singkat paper untuk preview")
    content = fields.Html('Abstrak', help="Abstrak lengkap paper konferensi")
    
    # Hide/override problematic blog fields dari parent blog.post
    cover_properties = fields.Text(string="Cover Properties", default='{}', readonly=True)
    teaser_manual = fields.Html(string="Teaser Manual", readonly=True)
    
    # Explicitly override other blog fields that might cause confusion
    website_meta_title = fields.Char(string="Meta Title", readonly=True)
    website_meta_description = fields.Text(string="Meta Description", readonly=True)
    website_meta_keywords = fields.Char(string="Meta Keywords", readonly=True)
    
    # Field khusus prosiding konferensi
    authors = fields.Char('Penulis', required=True)
    corresponding_author = fields.Char('Penulis Korespondensi')
    conference_name = fields.Char('Nama Konferensi', required=True)
    conference_acronym = fields.Char('Singkatan Konferensi', help="Contoh: ICICT, ICITACEE, dll")
    organizer = fields.Char('Penyelenggara')
    organizer_website = fields.Char('Website Penyelenggara')
    conference_date = fields.Date('Tanggal Konferensi', required=True)
    
    # Conference location
    conference_city = fields.Char('Kota Konferensi')
    conference_country = fields.Char('Negara Konferensi')
    conference_venue = fields.Char('Tempat Konferensi')
    
    # Publication details
    publisher = fields.Char('Penerbit', help="IEEE, ACM, Springer, Elsevier, dll")
    proceedings_title = fields.Char('Judul Prosiding')
    volume = fields.Char('Volume')
    pages = fields.Char('Halaman', help="Contoh: 123-145")
    isbn = fields.Char('ISBN')
    doi = fields.Char('DOI', help="Digital Object Identifier")
    url = fields.Char('URL Paper', help="Link ke paper online")
    
    # Conference type & classification
    conference_type = fields.Selection([
        ('symposium', 'Symposium'),
        ('workshop', 'Workshop'), 
        ('conference', 'Conference'),
        ('congress', 'Congress'),
        ('seminar', 'Seminar'),
        ('colloquium', 'Colloquium'),
    ], string='Jenis Acara', default='conference')
    
    presentation_type = fields.Selection([
        ('oral', 'Presentasi Oral'),
        ('poster', 'Poster'),
        ('keynote', 'Keynote Speaker'),
        ('invited', 'Invited Speaker'),
        ('panel', 'Panel Discussion'),
    ], string='Jenis Presentasi', default='oral')
    
    # Quality & Indexing
    conference_rank = fields.Selection([
        ('A*', 'A* (Top-tier)'),
        ('A', 'A (Excellent)'),
        ('B', 'B (Good)'),
        ('C', 'C (Fair)'),
        ('unranked', 'Unranked'),
    ], string='Peringkat Konferensi')
    
    # Indexing flags
    ieee_indexed = fields.Boolean('IEEE Xplore')
    acm_indexed = fields.Boolean('ACM Digital Library')
    scopus_indexed = fields.Boolean('Terindeks Scopus')
    wos_indexed = fields.Boolean('Terindeks Web of Science')
    sinta_indexed = fields.Boolean('Terindeks SINTA')
    
    sinta_rank = fields.Selection([
        ('1', 'SINTA 1'),
        ('2', 'SINTA 2'),
        ('3', 'SINTA 3'),
        ('4', 'SINTA 4'),
        ('5', 'SINTA 5'),
        ('6', 'SINTA 6')
    ], string='Peringkat SINTA')
    
    # Subject classification
    subject_area = fields.Char('Bidang Subjek')
    research_area = fields.Text('Area Penelitian')
    keywords = fields.Text('Kata Kunci', help="Kata kunci dipisahkan dengan koma")
    
    # Track/Session info
    track_name = fields.Char('Nama Track/Session')
    session_chair = fields.Char('Ketua Session')
    
    # Computed fields
    conference_year = fields.Integer('Tahun Konferensi', compute='_compute_conference_year', store=True)
    
    # Citation metrics
    citations = fields.Integer('Jumlah Sitasi', default=0)
    
    # Award/recognition
    best_paper = fields.Boolean('Best Paper Award')
    award_description = fields.Char('Deskripsi Penghargaan')
    
    @api.depends('name')
    def _compute_slug(self):
        for record in self:
            if not record.slug and record.name:
                import re
                # Convert to lowercase and replace special characters
                slug = record.name.lower()
                slug = re.sub(r'[^a-z0-9\s-]', '', slug)
                slug = re.sub(r'\s+', '-', slug)
                slug = slug.strip('-')
                record.slug = slug
            else:
                record.slug = ''
    def _inverse_slug(self):
        for record in self:
            # Kalau user mengubah slug secara manual, simpan apa adanya
            if record.slug:
                record.slug = record.slug.strip().lower().replace(' ', '-')

    @api.depends('conference_date')
    def _compute_conference_year(self):
        for record in self:
            if record.conference_date:
                record.conference_year = record.conference_date.year
            else:
                record.conference_year = datetime.now().year
    
    # Override website URL untuk halaman khusus dengan SEO-friendly URL
    def _compute_website_url(self):
        super(ProsidingPost, self)._compute_website_url()
        for post in self:
            if post.id and post.blog_id and post.slug:
                post.website_url = f"/prosiding/paper/{post.slug}-{post.id}"
            elif post.id and post.blog_id:
                post.website_url = f"/prosiding/paper/{post.id}"
    
    def get_meta_title(self):
        """Get meta title for SEO"""
        return self.meta_title or self.name
    
    def get_meta_description(self):
        """Get meta description for SEO"""
        return self.meta_description or self.teaser or f"Paper konferensi: {self.name}"
    
    def get_meta_keywords(self):
        """Get meta keywords for SEO"""
        if self.meta_keywords:
            return self.meta_keywords
        keywords = []
        if self.authors:
            keywords.extend(self.authors.split(',')[:2])  # First 2 authors
        if self.conference_name:
            keywords.append(self.conference_name)
        if self.subject_area:
            keywords.append(self.subject_area)
        if self.conference_acronym:
            keywords.append(self.conference_acronym)
        return ', '.join(keywords) if keywords else ''
    
    def get_indexing_badges(self):
        """Return list of indexing badges for display"""
        badges = []
        if self.ieee_indexed:
            badges.append({'name': 'IEEE Xplore', 'class': 'badge-primary'})
        if self.acm_indexed:
            badges.append({'name': 'ACM DL', 'class': 'badge-info'})
        if self.scopus_indexed:
            badges.append({'name': 'Scopus', 'class': 'badge-success'})
        if self.wos_indexed:
            badges.append({'name': 'Web of Science', 'class': 'badge-warning'})
        if self.sinta_indexed and self.sinta_rank:
            badges.append({'name': f'SINTA {self.sinta_rank}', 'class': 'badge-secondary'})
        return badges
    
    def get_conference_location(self):
        """Get formatted conference location"""
        location_parts = []
        if self.conference_city:
            location_parts.append(self.conference_city)
        if self.conference_country:
            location_parts.append(self.conference_country)
        return ', '.join(location_parts) if location_parts else ''
    
    def button_publish(self):
        """Publikasikan prosiding ke website"""
        for record in self:
            record.website_published = True
            record.publication_date = fields.Datetime.now()
        return True
    
    def button_unpublish(self):
        """Batalkan publikasi prosiding dari website"""
        for record in self:
            record.website_published = False
        return True