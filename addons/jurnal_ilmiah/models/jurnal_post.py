# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class JurnalPost(models.Model):
    _name = 'jurnal.post'
    _inherit = 'blog.post'
    _description = 'Entri Jurnal Ilmiah'
    
    # Override fields dari blog post
    name = fields.Char('Judul Artikel', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul atau judul kecil")
    blog_id = fields.Many2one('jurnal.blog', 'Kategori Jurnal', required=True, ondelete='cascade')
        
    # Override blog fields dengan label yang jelas untuk jurnal
    teaser = fields.Text('Sinopsis', help="Ringkasan singkat artikel untuk preview")
    content = fields.Html('Abstrak', help="Abstrak lengkap artikel jurnal")
    
    # Hide/override problematic blog fields dari parent blog.post
    cover_properties = fields.Text(string="Cover Properties", default='{}', readonly=True)
    teaser_manual = fields.Html(string="Teaser Manual", readonly=True)
    
    # Explicitly override other blog fields that might cause confusion
    website_meta_title = fields.Char(string="Meta Title", readonly=True)
    website_meta_description = fields.Text(string="Meta Description", readonly=True)
    website_meta_keywords = fields.Char(string="Meta Keywords", readonly=True)
    
    # Field khusus jurnal ilmiah
    authors = fields.Char('Penulis', required=True)
    corresponding_author = fields.Char('Penulis Korespondensi')
    journal_name = fields.Char('Nama Jurnal', required=True)
    publisher = fields.Char('Penerbit')
    publication_date = fields.Date('Tanggal Publikasi', default=fields.Date.today)
    
    # Publication details
    volume = fields.Char('Volume')
    issue = fields.Char('Issue/Nomor')
    pages = fields.Char('Halaman', help="Contoh: 123-145")
    doi = fields.Char('DOI', help="Digital Object Identifier")
    url = fields.Char('URL Jurnal', help="Link ke artikel online")
    
    # Impact & Indexing
    impact_factor = fields.Float('Impact Factor', digits=(5, 3))
    h_index = fields.Integer('H-Index')
    quartile = fields.Selection([
        ('Q1', 'Q1 (Top 25%)'),
        ('Q2', 'Q2 (25-50%)'),
        ('Q3', 'Q3 (50-75%)'),
        ('Q4', 'Q4 (Bottom 25%)')
    ], string='Quartile')
    
    # Indexing flags
    scopus_indexed = fields.Boolean('Terindeks Scopus')
    wos_indexed = fields.Boolean('Terindeks Web of Science')
    sinta_indexed = fields.Boolean('Terindeks SINTA')
    doaj_indexed = fields.Boolean('Terindeks DOAJ')
    
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
    
    # Computed fields
    publication_year = fields.Integer('Tahun Publikasi', compute='_compute_publication_year', store=True)
    
    # Citation metrics
    citations = fields.Integer('Jumlah Sitasi', default=0)
    # downloads field removed - tidak relevan untuk artikel jurnal yang di-host di publisher
    
    @api.depends('publication_date')
    def _compute_publication_year(self):
        for record in self:
            if record.publication_date:
                record.publication_year = record.publication_date.year
            else:
                record.publication_year = datetime.now().year
    
    # Override website URL untuk halaman khusus
    def _compute_website_url(self):
        super(JurnalPost, self)._compute_website_url()
        for post in self:
            if post.id and post.blog_id:
                post.website_url = f"/jurnal/artikel/{post.id}"
    
    def get_indexing_badges(self):
        """Return list of indexing badges for display"""
        badges = []
        if self.scopus_indexed:
            badges.append({'name': 'Scopus', 'class': 'badge-primary'})
        if self.wos_indexed:
            badges.append({'name': 'Web of Science', 'class': 'badge-success'})
        if self.sinta_indexed and self.sinta_rank:
            badges.append({'name': f'SINTA {self.sinta_rank}', 'class': 'badge-info'})
        if self.doaj_indexed:
            badges.append({'name': 'DOAJ', 'class': 'badge-warning'})
        return badges
    
    def get_impact_info(self):
        """Return impact factor information"""
        info = {}
        if self.impact_factor:
            info['impact_factor'] = self.impact_factor
        if self.quartile:
            info['quartile'] = self.quartile
        if self.h_index:
            info['h_index'] = self.h_index
        return info