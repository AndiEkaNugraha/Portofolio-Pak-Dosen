# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class MatakuliahController(http.Controller):
    @http.route('/mata-kuliah', type='http', auth='public', website=True)
    def index(self, **kw):
        courses = request.env['matakuliah.post'].sudo().search([])
        return request.render('matakuliah.courses_list', {
            'courses': courses
        })

    @http.route(['/mata-kuliah/<model("matakuliah.post"):course>'], type='http', auth="public", website=True)
    def matakuliah_detail(self, course, **kwargs):
        values = {
            'course': course
        }
        return request.render('matakuliah.matakuliah_detail_template', values)