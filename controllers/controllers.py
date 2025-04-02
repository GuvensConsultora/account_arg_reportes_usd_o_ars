# -*- coding: utf-8 -*-
# from odoo import http


# class FacturaEnUsd(http.Controller):
#     @http.route('/factura_en_usd/factura_en_usd', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/factura_en_usd/factura_en_usd/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('factura_en_usd.listing', {
#             'root': '/factura_en_usd/factura_en_usd',
#             'objects': http.request.env['factura_en_usd.factura_en_usd'].search([]),
#         })

#     @http.route('/factura_en_usd/factura_en_usd/objects/<model("factura_en_usd.factura_en_usd"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('factura_en_usd.object', {
#             'object': obj
#         })

