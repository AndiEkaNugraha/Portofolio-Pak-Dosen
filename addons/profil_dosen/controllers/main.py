# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ProfilDosenController(http.Controller):
    """
    Controller untuk menampilkan halaman profil dosen di website
    """

    @http.route('/profil-dosen', auth='public', website=True, sitemap=True)
    def profil_dosen_page(self, **kwargs):
        """
        Halaman profil dosen single page
        URL: /profil-dosen
        """
        # Ambil record profil dosen yang dipublikasikan (aktif)
        dosen = request.env['profil.dosen'].sudo().search([
            ('is_published', '=', True),
            ('active', '=', True)
        ], limit=1, order='sequence, create_date')

        if not dosen:
            # Jika tidak ada dosen yang dipublikasikan, ambil yang pertama
            dosen = request.env['profil.dosen'].sudo().search([
                ('active', '=', True)
            ], limit=1, order='sequence, create_date')

        if not dosen:
            return request.render('website.404')

        # Siapkan data untuk template
        values = {
            'dosen': dosen,
        }

        # Render template
        return request.render('profil_dosen.profil_dosen_page', values)

    @http.route('/profil-dosen/<string:slug>', auth='public', website=True, sitemap=True)
    def profil_dosen_by_slug(self, slug, **kwargs):
        """
        Halaman profil dosen berdasarkan slug (untuk kemungkinan multi-dosen di masa depan)
        URL: /profil-dosen/nama-dosen
        """
        dosen = request.env['profil.dosen'].sudo().search([
            ('slug', '=', slug),
            ('is_published', '=', True),
            ('active', '=', True)
        ], limit=1)

        if not dosen:
            return request.render('website.404')

        values = {
            'dosen': dosen,
        }

        return request.render('profil_dosen.profil_dosen_page', values)

    @http.route('/profil-dosen/<int:dosen_id>/download-cv', auth='public', website=True)
    def download_cv(self, dosen_id, **kwargs):
        """
        Download file CV
        """
        dosen = request.env['profil.dosen'].sudo().browse(dosen_id)

        if not dosen.cv_file or not dosen.is_published:
            return request.render('website.404')

        # Return file download
        return http.request.make_response(
            dosen.cv_file,
            headers=[
                ('Content-Disposition', f'attachment; filename="{dosen.cv_filename}"'),
                ('Content-Type', 'application/pdf'),
            ]
        )
