from odoo import http
from odoo.http import request
from odoo.exceptions import NotFound


class JadwalKonsultasiController(http.Controller):
    """Controller untuk halaman website jadwal konsultasi"""

    @http.route('/jadwal-konsultasi', auth='public', website=True, sitemap=True)
    def jadwal_konsultasi_list(self, **post):
        """Tampilkan daftar jadwal konsultasi"""
        # Ambil semua jadwal yang aktif dan dipublikasikan
        schedules = request.env['jadwal.konsultasi'].sudo().search([
            ('is_active', '=', True),
            ('website_published', '=', True)
        ], order='hari_konsultasi asc, jam_mulai asc')

        # Apply filters jika ada
        jenis_filter = post.get('jenis_konsultasi')
        if jenis_filter:
            schedules = schedules.filtered(lambda s: s.jenis_konsultasi == jenis_filter)

        hari_filter = post.get('hari_konsultasi')
        if hari_filter:
            schedules = schedules.filtered(lambda s: str(s.hari_konsultasi) == hari_filter)

        tipe_lokasi_filter = post.get('tipe_lokasi')
        if tipe_lokasi_filter:
            schedules = schedules.filtered(lambda s: s.tipe_lokasi == tipe_lokasi_filter)

        # Increment view count
        for schedule in schedules:
            schedule.view_count += 1

        return request.render('jadwal_konsultasi.jadwal_konsultasi_list', {
            'schedules': schedules,
        })

    @http.route('/jadwal-konsultasi/<slug>', auth='public', website=True, sitemap=True)
    def jadwal_konsultasi_detail(self, slug, **post):
        """Tampilkan detail jadwal konsultasi"""
        # Cari jadwal berdasarkan slug
        schedule = request.env['jadwal.konsultasi'].sudo().search([
            ('slug', '=', slug),
            ('is_active', '=', True),
            ('website_published', '=', True)
        ], limit=1)

        if not schedule:
            raise NotFound("Jadwal konsultasi tidak ditemukan")

        # Increment view count
        schedule.view_count += 1

        return request.render('jadwal_konsultasi.jadwal_konsultasi_detail', {
            'schedule': schedule,
        })

    @http.route('/jadwal-konsultasi/<slug>/availability', auth='public', website=True, type='json')
    def jadwal_konsultasi_availability(self, slug, **post):
        """API untuk check ketersediaan jadwal (AJAX)"""
        schedule = request.env['jadwal.konsultasi'].sudo().search([
            ('slug', '=', slug),
            ('is_active', '=', True),
        ], limit=1)

        if not schedule:
            return {'status': 'error', 'message': 'Jadwal tidak ditemukan'}

        return {
            'status': 'success',
            'is_available': not schedule.is_kuota_penuh(),
            'kuota_tersedia': schedule.kuota_tersedia,
            'kapasitas_maksimal': schedule.kapasitas_maksimal,
            'is_active': schedule.is_active,
        }

    @http.route('/jadwal-konsultasi/<slug>/book', auth='user', website=True, methods=['POST'], type='json')
    def jadwal_konsultasi_book(self, slug, **post):
        """Handle booking konsultasi (untuk mahasiswa)"""
        schedule = request.env['jadwal.konsultasi'].sudo().search([
            ('slug', '=', slug),
            ('is_active', '=', True),
        ], limit=1)

        if not schedule:
            return {'status': 'error', 'message': 'Jadwal tidak ditemukan'}

        if schedule.is_kuota_penuh():
            return {'status': 'error', 'message': 'Kuota sudah penuh'}

        try:
            # Increment peserta (dapat ditambahkan ke model untuk tracking booking)
            schedule.peserta_terdaftar += 1
            return {
                'status': 'success',
                'message': 'Berhasil mendaftar konsultasi',
                'kuota_tersedia': schedule.kuota_tersedia,
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
