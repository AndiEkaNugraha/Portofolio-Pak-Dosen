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
    
    # SEO fields
    slug = fields.Char('URL Slug', index=True, help="URL slug yang SEO-friendly. Kosongkan untuk generate otomatis dari judul.")
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan judul artikel jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan sinopsis jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
        
    # Override blog fields dengan label yang jelas untuk jurnal
    teaser = fields.Char('Sinopsis', help="Ringkasan singkat artikel untuk preview")
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
    publisher_website = fields.Char('Situs Penerbit')
    
    # Publication details
    volume = fields.Char('Volume')
    issue = fields.Char('Issue/Nomor')
    pages = fields.Char('Halaman', help="Contoh: 123-145")
    doi = fields.Char('DOI', help="Digital Object Identifier")
    url = fields.Char('URL Jurnal', help="Link ke jurnal online")
    
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
    
    def _generate_slug_from_name(self, name):
        """Generate SEO-friendly slug from name"""
        if not name:
            return ''
        import re
        # Convert to lowercase and replace special characters
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    @api.model
    def create(self, vals_list):
        """Auto-generate slug if not provided"""
        # Handle both single dict and list of dicts
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            if not vals.get('slug') and vals.get('name'):
                vals['slug'] = self._generate_slug_from_name(vals['name'])
                # Ensure uniqueness
                vals['slug'] = self._ensure_unique_slug(vals['slug'])
        
        return super(JurnalPost, self).create(vals_list)
    
    def write(self, vals):
        """Auto-regenerate slug if name changed and slug is empty"""
        if 'name' in vals and not vals.get('slug'):
            for record in self:
                if not record.slug:  # Only if slug is currently empty
                    vals['slug'] = self._generate_slug_from_name(vals.get('name', record.name))
                    vals['slug'] = record._ensure_unique_slug(vals['slug'], exclude_id=record.id)
        return super(JurnalPost, self).write(vals)
    
    def _ensure_unique_slug(self, slug, exclude_id=None):
        """Ensure slug is unique by adding number suffix if needed"""
        if not slug:
            return slug
            
        domain = [('slug', '=', slug)]
        if exclude_id:
            domain.append(('id', '!=', exclude_id))
            
        if self.search_count(domain) == 0:
            return slug
            
        # Add number suffix to make it unique
        counter = 1
        original_slug = slug
        while self.search_count([('slug', '=', slug)] + ([('id', '!=', exclude_id)] if exclude_id else [])) > 0:
            slug = f"{original_slug}-{counter}"
            counter += 1
        return slug
    
    @api.depends('publication_date')
    def _compute_publication_year(self):
        for record in self:
            if record.publication_date:
                record.publication_year = record.publication_date.year
            else:
                record.publication_year = datetime.now().year
    
    # Override website URL untuk halaman khusus dengan SEO-friendly URL
    def _compute_website_url(self):
        super(JurnalPost, self)._compute_website_url()
        for post in self:
            if post.id and post.blog_id and post.slug:
                post.website_url = f"/jurnal/artikel/{post.slug}-{post.id}"
            elif post.id and post.blog_id:
                post.website_url = f"/jurnal/artikel/{post.id}"
    
    def get_meta_title(self):
        """Get meta title for SEO"""
        return self.meta_title or self.name
    
    def get_meta_description(self):
        """Get meta description for SEO"""
        return self.meta_description or self.teaser or f"Artikel jurnal: {self.name}"
    
    def get_meta_keywords(self):
        """Get meta keywords for SEO"""
        if self.meta_keywords:
            return self.meta_keywords
        keywords = []
        if self.authors:
            keywords.extend(self.authors.split(',')[:2])  # First 2 authors
        if self.journal_name:
            keywords.append(self.journal_name)
        if self.subject_area:
            keywords.append(self.subject_area)
        return ', '.join(keywords) if keywords else ''
    
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
    
    @api.constrains('slug')
    def _check_slug_format(self):
        """Validate slug format"""
        for record in self:
            if record.slug:
                import re
                if not re.match(r'^[a-z0-9-]+$', record.slug):
                    raise ValueError("Slug hanya boleh mengandung huruf kecil, angka, dan tanda hubung (-)")
                if record.slug.startswith('-') or record.slug.endswith('-'):
                    raise ValueError("Slug tidak boleh diawali atau diakhiri dengan tanda hubung (-)")
                if '--' in record.slug:
                    raise ValueError("Slug tidak boleh mengandung tanda hubung ganda (--)")
    
    @api.onchange('name')
    def _onchange_name_generate_slug(self):
        """Auto-generate slug when name changes if slug is empty"""
        if self.name and not self.slug:
            self.slug = self._generate_slug_from_name(self.name)