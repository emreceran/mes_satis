# -*- coding: utf-8 -*-
# from odoo import http


# class MesSatis(http.Controller):
#     @http.route('/mes_satis/mes_satis', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mes_satis/mes_satis/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mes_satis.listing', {
#             'root': '/mes_satis/mes_satis',
#             'objects': http.request.env['mes_satis.mes_satis'].search([]),
#         })

#     @http.route('/mes_satis/mes_satis/objects/<model("mes_satis.mes_satis"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mes_satis.object', {
#             'object': obj
#         })
