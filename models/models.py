# -*- coding: utf-8 -*-

from odoo import models, fields, api



# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin = fields.Float(
        "Margin", compute='_compute_margin',
        digits='Product Price', store=True, groups="base.group_user", precompute=True)
    margin_percent = fields.Float(
        "Margin (%)", compute='_compute_margin', store=True, groups="base.group_user", precompute=True)
    purchase_price = fields.Float(
        string="Cost", compute="_compute_purchase_price",
        digits='Product Price', store=True, readonly=False, precompute=True,
        groups="base.group_user")

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
    def _compute_purchase_price(self):
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            product_cost = line.product_id.standard_price
            line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)

    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            line.margin = line.price_subtotal - (line.purchase_price * line.product_uom_qty)
            # line.margin_percent = line.price_subtotal and line.margin/line.price_subtotal
            if line.purchase_price == 0:
                line.margin_percent =100
            else:
                line.margin_percent = line.price_subtotal and (line.margin/line.product_uom_qty)/line.purchase_price

    def _convert_price2(self, product_cost, from_uom):
        self.ensure_one()
        if not product_cost:
            # If the standard_price is 0
            # Avoid unnecessary computations
            # and currency conversions
            if not self.purchase_price:
                return product_cost
        from_currency = self.env["res.currency"].search([("id","=","1")])
        print("asa")
        # from_currency = self.product_id.cost_currency_id
        to_cur =  self.env["res.currency"].search([("id","=","31")])
        # to_cur = self.currency_id or self.order_id.currency_id
        to_uom = self.product_uom
        if to_uom and to_uom != from_uom:
            product_cost = from_uom._compute_price(
                product_cost,
                to_uom,
            )
        return from_currency._convert(
            from_amount=product_cost,
            to_currency=to_cur,
            company=self.company_id or self.env.company,
            date=self.order_id.date_order or fields.Date.today(),
            round=False,
        ) if to_cur and product_cost else product_cost
        # The pricelist may not have been set, therefore no conversion
        # is needed because we don't know the target currency..

    # def _prepare_invoice_line(self, **optional_values):
    #     """Prepare the values to create the new invoice line for a sales order line.
    #
    #     :param optional_values: any parameter that should be added to the returned invoice line
    #     :rtype: dict
    #     """
    #     self.ensure_one()
    #     res = {
    #         'display_type': self.display_type or 'product',
    #         'sequence': self.sequence,
    #         'name': self.name,
    #         'product_id': self.product_id.id,
    #         'product_uom_id': self.product_uom.id,
    #         'quantity': self.qty_to_invoice,
    #         'discount': self.discount,
    #         'price_unit': self.price_unit,
    #         'tax_ids': [Command.set(self.tax_id.ids)],
    #         'sale_line_ids': [Command.link(self.id)],
    #         'is_downpayment': self.is_downpayment,
    #     }
    #     analytic_account_id = self.order_id.analytic_account_id.id
    #     print(self.currency_id.id)
    #     res["price_unit"] = self._convert_price2(self.price_unit, self.product_id.uom_id)
    #     if self.analytic_distribution and not self.display_type:
    #         res['analytic_distribution'] = self.analytic_distribution
    #     if analytic_account_id and not self.display_type:
    #         if 'analytic_distribution' in res:
    #             res['analytic_distribution'][analytic_account_id] = res['analytic_distribution'].get(
    #                 analytic_account_id, 0) + 100
    #         else:
    #             res['analytic_distribution'] = {analytic_account_id: 100}
    #     if optional_values:
    #         res.update(optional_values)
    #     if self.display_type:
    #         res['account_id'] = False
    #     return res

"""
class sozen_reports(models.Model):
    _inherit='project.project'

    def get_panel_data(self):
        self.ensure_one()
        if not self.user_has_groups('base.group_system'):
        # if not self.user_has_groups('project.group_project_user'):
            return {}
        panel_data = {
            'user': self._get_user_values(),
            'buttons': sorted(self._get_stat_buttons(), key=lambda k: k['sequence']),
            'currency_id': self.currency_id.id,
        }
        if self.allow_milestones:
            panel_data['milestones'] = self._get_milestones()
        if self._show_profitability():
            profitability_items = self._get_profitability_items()
            if self._get_profitability_sequence_per_invoice_type() and profitability_items and 'revenues' in profitability_items and 'costs' in profitability_items:  # sort the data values
                profitability_items['revenues']['data'] = sorted(profitability_items['revenues']['data'], key=lambda k: k['sequence'])
                profitability_items['costs']['data'] = sorted(profitability_items['costs']['data'], key=lambda k: k['sequence'])
            panel_data['profitability_items'] = profitability_items
            panel_data['profitability_labels'] = self._get_profitability_labels()
        return panel_data
"""

# class mes_satis(models.Model):
#     _name = 'mes_satis.mes_satis'
#     _description = 'mes_satis.mes_satis'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
