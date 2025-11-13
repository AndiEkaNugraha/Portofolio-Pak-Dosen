# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class ProfilePost(models.Model):
    _name = 'profile.post'
    _description = 'Entri Profile Dosen'
    _order = 'sequence, id desc'
    
    _sql_constraints = [
        ('unique_author', 'UNIQUE(author_id)', 
         'Setiap user hanya boleh memiliki satu profile!'),
    ]
    
    # Basic fields
    name = fields.Char('Judul/Nama', required=True, translate=True)
    subtitle = fields.Char(string='Sub Judul', translate=True, help="Sub judul atau deskripsi singkat")
    blog_id = fields.Many2one('profile.blog', 'Kategori Profile', required=True, ondelete='cascade')
    sequence = fields.Integer('Urutan', default=10, help="Urutan tampilan di website")
    
    # SEO fields
    meta_title = fields.Char('Meta Title', help="Judul untuk SEO (akan menggunakan judul jika kosong)")
    meta_description = fields.Text('Meta Description', help="Deskripsi untuk SEO (akan menggunakan ringkasan jika kosong)")
    meta_keywords = fields.Char('Meta Keywords', help="Kata kunci untuk SEO, pisahkan dengan koma")
        
    # Content fields
    teaser = fields.Text('Ringkasan', help="Ringkasan singkat untuk preview dan website")
    content = fields.Html('Konten Lengkap', help="Konten lengkap profile", sanitize=False)
    
    # Cover photo
    cover_image = fields.Binary('Foto', attachment=True, help="Foto untuk profile item")
    cover_image_filename = fields.Char('Nama File')
    
    # Publication fields 
    is_published = fields.Boolean('Tampilkan di Website', default=True, help="Centang untuk menampilkan di website portofolio")
    active = fields.Boolean('Active', default=True)
    website_published = fields.Boolean('Published on Website', related='is_published', readonly=True)
    
    # Author
    author_id = fields.Many2one('res.users', 'Pemilik Profile', required=True, default=lambda self: self.env.user, help="User yang memiliki profile ini")
    
    # Default CV Template
    default_cv_template_id = fields.Many2one('cv.template', 'Template CV Default', 
                                             help="Template CV yang akan digunakan secara default saat generate CV")
    
    # Audit fields
    create_date = fields.Datetime('Created on', readonly=True)
    write_date = fields.Datetime('Last Updated on', readonly=True)
    create_uid = fields.Many2one('res.users', 'Created by', readonly=True)
    write_uid = fields.Many2one('res.users', 'Last Updated by', readonly=True)
    
    # Relations to specific profile types
    education_ids = fields.One2many('profile.education', 'profile_post_id', string='Riwayat Pendidikan')
    work_ids = fields.One2many('profile.work', 'profile_post_id', string='Riwayat Pekerjaan')
    award_ids = fields.One2many('profile.award', 'profile_post_id', string='Penghargaan')
    expertise_ids = fields.One2many('profile.expertise', 'profile_post_id', string='Bidang Keahlian')
    
    # CV Document
    cv_document = fields.Binary('Dokumen CV', attachment=True, help="Upload dokumen CV jika ada")
    cv_document_filename = fields.Char('Nama File CV')
    cv_generated_date = fields.Datetime('Tanggal CV Dibuat', readonly=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to enforce one profile per user"""
        for vals in vals_list:
            author_id = vals.get('author_id', self.env.uid)
            existing = self.search([('author_id', '=', author_id)], limit=1)
            if existing:
                raise ValidationError(_(
                    'Anda sudah memiliki profile! Silakan edit profile yang ada.\n'
                    'Profile: %s') % existing.name)
        return super().create(vals_list)
    
    def get_meta_title(self):
        """Get meta title for SEO"""
        return self.meta_title or self.name
    
    def get_meta_description(self):
        """Get meta description for SEO"""
        return self.meta_description or self.teaser or f"Profile: {self.name}"
    
    def action_generate_cv(self):
        """Action to generate CV from all data"""
        self.ensure_one()
        cv_generator = self.env['cv.generator'].create({
            'profile_post_id': self.id,
        })
        return cv_generator.generate_cv()
    
    def action_download_cv(self):
        """Action to download generated CV"""
        self.ensure_one()
        if not self.cv_document:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Tidak Ada CV',
                    'message': 'CV belum di-generate. Silakan generate CV terlebih dahulu.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/profile.post/{self.id}/cv_document?download=true',
            'target': 'new',
        }
    
    def action_reset_biography(self):
        """Reset field content ke biography default dari data XML"""
        self.ensure_one()
        
        # Ambil external ID untuk profile_post_main
        external_id = self.env['ir.model.data'].search([
            ('model', '=', 'profile.post'),
            ('res_id', '=', self.id)
        ], limit=1)
        
        if not external_id or external_id.name != 'profile_post_main':
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Tidak Bisa Reset',
                    'message': 'Hanya profile utama dari data bawaan yang bisa direset.',
                    'type': 'warning',
                }
            }
        
        # Biography default dari profile_data.xml
        default_biography = """
                    <h2>Tentang Saya</h2>
                    <p>Dr. Ahmad Hidayat adalah dosen dan peneliti di Program Studi Informatika, Fakultas Teknik, Universitas Islam Indonesia. Dengan latar belakang pendidikan S3 Ilmu Komputer dari Universitas Teknologi Bandung, beliau memiliki keahlian mendalam di bidang Machine Learning, Deep Learning, Natural Language Processing, dan Computer Vision.</p>
                    
                    <p>Perjalanan akademik dimulai dari pendidikan S1 Teknik Informatika di Universitas Gadjah Mada (2008-2012), dilanjutkan dengan S2 di Institut Teknologi Sepuluh Nopember (2012-2014), dan meraih gelar doktor dari Universitas Teknologi Bandung (2015-2019) dengan disertasi tentang Deep Learning untuk pemrosesan bahasa Indonesia.</p>
                    
                    <h2>Fokus Penelitian</h2>
                    <p>Fokus penelitian saya adalah pengembangan model Machine Learning dan Deep Learning untuk aplikasi praktis, khususnya dalam konteks bahasa Indonesia. Beberapa area penelitian utama meliputi:</p>
                    <ul>
                        <li><strong>Natural Language Processing (NLP)</strong>: Pengembangan model untuk text mining, sentiment analysis, named entity recognition, dan language modeling khusus bahasa Indonesia</li>
                        <li><strong>Computer Vision</strong>: Aplikasi deep learning untuk deteksi objek, klasifikasi gambar, dan pengenalan pola</li>
                        <li><strong>Machine Learning Applications</strong>: Implementasi ML untuk berbagai domain seperti healthcare, education, dan business intelligence</li>
                        <li><strong>AI Ethics & Responsible AI</strong>: Penelitian tentang aspek etika dan keadilan dalam sistem AI</li>
                    </ul>
                    
                    <h2>Pengalaman Profesional</h2>
                    <p>Sebelum menjadi dosen tetap di Universitas Islam Indonesia (2019-sekarang), saya memiliki pengalaman sebagai dosen luar biasa di Universitas Gadjah Mada (2014-2019) dan bekerja di industri teknologi sebagai Machine Learning Engineer di PT Teknologi Cerdas Indonesia (2012-2014). Pengalaman ini memberikan perspektif yang seimbang antara teori akademik dan implementasi praktis di industri.</p>
                    
                    <h2>Kontribusi Akademik</h2>
                    <p>Hingga saat ini, saya telah mempublikasikan lebih dari 45 artikel di jurnal internasional bereputasi dan konferensi internasional. Beberapa publikasi telah mendapat penghargaan best paper dan banyak dikutip oleh peneliti lain di seluruh dunia. Saya juga aktif sebagai reviewer untuk berbagai jurnal internasional dan konferensi IEEE.</p>
                    
                    <p>Dalam hal pengajaran, saya mengampu mata kuliah Machine Learning, Deep Learning, Artificial Intelligence, Algoritma dan Pemrograman, serta Struktur Data. Pendekatan pengajaran saya mengkombinasikan teori yang kuat dengan praktik langsung menggunakan tools dan framework terkini seperti TensorFlow, PyTorch, dan scikit-learn.</p>
                    
                    <h2>Pembimbingan Mahasiswa</h2>
                    <p>Saya sangat antusias dalam membimbing mahasiswa S1 dan S2 untuk menghasilkan penelitian berkualitas. Hingga kini, telah membimbing lebih dari 60 mahasiswa S1 untuk tugas akhir dan 15 mahasiswa S2 untuk tesis. Beberapa mahasiswa bimbingan berhasil mempublikasikan hasil penelitiannya di konferensi internasional dan memenangkan kompetisi ilmiah nasional.</p>
                    
                    <h2>Pengabdian Masyarakat</h2>
                    <p>Selain mengajar dan meneliti, saya juga aktif dalam kegiatan pengabdian masyarakat, terutama dalam bentuk pelatihan dan workshop tentang AI, Data Science, dan Python Programming untuk kalangan akademisi, praktisi industri, serta guru-guru SMK. Saya percaya bahwa teknologi AI harus dapat dimanfaatkan secara luas untuk meningkatkan kesejahteraan masyarakat.</p>
                    
                    <h2>Visi ke Depan</h2>
                    <p>Visi saya adalah terus berkontribusi dalam pengembangan ilmu pengetahuan di bidang Artificial Intelligence, khususnya yang relevan dengan konteks Indonesia. Saya berkomitmen untuk menghasilkan penelitian berkualitas tinggi, mendidik generasi peneliti dan praktisi AI yang kompeten, serta memastikan pengembangan AI yang etis dan bermanfaat bagi masyarakat.</p>
                    
                    <h2>Hubungi Saya</h2>
                    <p>Saya terbuka untuk kolaborasi penelitian, konsultasi, dan diskusi seputar Machine Learning, AI, dan teknologi terkait. Jangan ragu untuk menghubungi melalui email atau media profesional lainnya.</p>
        """
        
        self.write({'content': default_biography.strip()})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Biography Direset',
                'message': 'Field "Konten Lengkap" telah direset ke biography default.',
                'type': 'success',
                'sticky': False,
            }
        }
