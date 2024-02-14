# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.
# from odoo import api, fields, models, _
#
#
# class accountmoveline(models.Model):
#     _inherit = "account.move"
#
#     order_line = fields.Many2one(
#         comodel_name='account.move.line',
#         index=True, required=True)
#
#     def _get_update_prices_lines(self):
#         """ Hook to exclude specific lines which should not be updated based on price list recomputation """
#         return self.order_line.filtered(lambda line: not line.display_type)
#
#     @api.onchange('currency_id')
#     def onchange_currency_id(self):
#
#         print("asa")
#         for order in self:
#             # order = order.with_company(order.company_id).with_context(lang=order.partner_invoice_id.lang)
#
#             # invoice_vals = order._prepare_invoice()
#             # invoiceable_lines = order._get_invoiceable_lines(final)
#
#             lines_to_recompute = self._get_update_prices_lines()
#             lines_to_recompute.invalidate_recordset(['currency_id'])
#             lines_to_recompute._compute_price_unit()
#
#
#             print(lines_to_recompute._compute_price_unit())
#
#
#
#
#
# #
# #
# # class SaleOrderLine(models.Model):
# #     _inherit = "sale.order.line"
# #
# #
# #     cost_discount = fields.Float("indirim", readonly=False, store=True, groups="base.group_user")
# #
# #
# #     std_price = fields.Float(
# #         string="Cost", compute="_compute_std_price",
# #         digits='Product Price', store=True, readonly=False, precompute=True,
# #         groups="base.group_user")
# #
# #     purchase_price = fields.Float(
# #         string="Cost", compute="_compute_purchase_price",
# #         digits='Product Price', store=True, readonly=False, precompute=True,
# #         groups="base.group_user")
# #
# #     @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
# #     def _compute_std_price(self):
# #         for line in self:
# #             if not line.product_id:
# #                 line.purchase_price = 0.0
# #                 continue
# #             line = line.with_company(line.company_id)
# #             product_cost = line.product_id.standard_price
# #             line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)
# #
# #     @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
# #     def _compute_purchase_price(self):
# #         for line in self:
# #             if not line.product_id:
# #                 line.purchase_price = 0.0
# #                 continue
# #             line = line.with_company(line.company_id)
# #             product_cost = line.product_id.adamsaat
# #             line.purchase_price = product_cost
# #
# #
# #     def _convert_price(self, product_cost, from_uom):
# #         self.ensure_one()
# #         if not product_cost:
# #             # If the standard_price is 0
# #             # Avoid unnecessary computations
# #             # and currency conversions
# #             if not self.purchase_price:
# #                 return product_cost
# #         from_currency = self.product_id.cost_currency_id
# #         to_cur = self.currency_id or self.order_id.currency_id
# #         to_uom = self.product_uom
# #         if to_uom and to_uom != from_uom:
# #             product_cost = from_uom._compute_price(
# #                 product_cost,
#     #             to_uom,
#     #         )
#     #     return from_currency._convert(
#     #         from_amount=product_cost,
#     #         to_currency=to_cur,
#     #         company=self.company_id or self.env.company,
#     #         date=self.order_id.date_order or fields.Date.today(),
#     #         round=False,
#     #     ) if to_cur and product_cost else product_cost
#     #     # The pricelist may not have been set, therefore no conversion
#     #     # is needed because we don't know the target currency..
#     #
#     #
#     # @api.onchange('cost_discount')
#     # def onchange_cost_discount(self):
#     #     # self.purchase_price = (1 - self.cost_discount/100) * self.purchase_price
#     #     # print(self.purchase_price)
#     #     for line in self:
#     #         line = line.with_company(line.company_id)
#     #         product_cost = line.product_id.standard_price
#     #         x = line._convert_price(product_cost, line.product_id.uom_id)
#     #         line.purchase_price = (1 - line.cost_discount / 100) * x
#     #         line.margin = line.price_subtotal - (line.price_unit * line.product_uom_qty)
#     #         print(line.purchase_price)
#     #
