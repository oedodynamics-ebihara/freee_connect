# -*- coding: utf-8 -*-

from odoo import http

class FreeeConect(http.Controller):
    @http.route('/freee_conect/freee_conect', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/freee_conect/freee_conect/objects', auth='public')
    def list(self, **kw):
        return http.request.render('freee_conect.listing', {
            'root': '/freee_conect/freee_conect',
            'objects': http.request.env['freee_conect.freee_conect'].search([]),
        })

    @http.route('/freee_conect/freee_conect/objects/<model("freee_conect.freee_conect"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('freee_conect.object', {
            'object': obj
        })
