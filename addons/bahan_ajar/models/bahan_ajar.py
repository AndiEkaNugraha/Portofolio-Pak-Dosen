# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class BahanAjarPost(models.Model):
    _inherit = 'blog.post'
    _description = 'Teaching Material Post'
    _order = 'sequence, name'

    sequence = fields.Integer('Sequence', default=10, help="Order in the materials list")
    file_type = fields.Selection([
        ('pdf', 'PDF Document'),
        ('video', 'Video Content'),
        ('link', 'Web Resource'),
    ], string='Content Type', required=True)
    
    # Fields based on file_type
    pdf_file = fields.Binary('PDF File', attachment=True)
    pdf_filename = fields.Char('PDF Filename')
    video_url = fields.Char('Video URL')
    web_resource_url = fields.Char('Resource URL')
    
    # Educational details
    topic = fields.Char('Topic/Subject Area', required=True, 
                       help="Main topic or subject area of the material")
    learning_objectives = fields.Text('Learning Objectives',
                                    help="What students will learn from this material")
    target_audience = fields.Selection([
        ('basic', 'Basic Level'),
        ('intermediate', 'Intermediate Level'),
        ('advanced', 'Advanced Level')
    ], string='Target Level', required=True, default='basic')
    estimated_time = fields.Float('Estimated Study Time (Hours)',
                                help="Estimated time needed to complete this material")
    prerequisites = fields.Text('Prerequisites',
                              help="Required knowledge or materials before studying this content")
    
    material_type = fields.Selection([
        ('lecture', 'Lecture Notes'),
        ('assignment', 'Assignment/Exercise'),
        ('reference', 'Reference Material'),
        ('supplementary', 'Supplementary Material'),
    ], string='Material Type', required=True)
    
    is_downloadable = fields.Boolean('Downloadable', default=True,
                                   help="Allow students to download this material")
    download_count = fields.Integer('Download Count', default=0, readonly=True)
    
    # Slug for URL
    slug = fields.Char('Slug', compute='_compute_slug', store=True, readonly=True)
    
    # Website URL
    website_url = fields.Char('Website URL', compute='_compute_website_url', readonly=True)

    @api.model
    def default_get(self, fields_list):
        """Set default values for new records"""
        res = super().default_get(fields_list)
        
        # Get or create blog_bahan_ajar
        blog_model = self.env['blog.blog']
        blog = blog_model.search([('id', '=', self.env.ref('bahan_ajar.blog_bahan_ajar').id)], limit=1)
        if blog:
            res['blog_id'] = blog.id
        
        # Set current user as author if not set
        if 'author_id' not in res or not res['author_id']:
            res['author_id'] = self.env.user.id
        
        return res
    
    @api.onchange('file_type')
    def _onchange_file_type(self):
        # Clear the fields of other types when type changes
        if self.file_type != 'pdf':
            self.pdf_file = False
            self.pdf_filename = False
        if self.file_type != 'video':
            self.video_url = False
        if self.file_type != 'link':
            self.web_resource_url = False
    
    def action_publish(self):
        self.write({'state': 'published'})
    
    def action_archive(self):
        self.write({'state': 'archived'})
    
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.depends('name')
    def _compute_slug(self):
        for record in self:
            if record.name:
                record.slug = record.name.lower().replace(' ', '-').replace('/', '-')

    @api.depends('slug')
    def _compute_website_url(self):
        for record in self:
            if record.slug:
                record.website_url = f'/bahan-ajar/{record.slug}'