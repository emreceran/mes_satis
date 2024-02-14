# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    margin = fields.Monetary("Margin", compute='_compute_margint', store=True)
    margin_percent = fields.Float("Margin (%)", compute='_compute_margint', store=True, group_operator="avg")

    @api.depends('order_line.margin', 'amount_untaxed')
    def _compute_margint(self):

        for rec in self:
            toplam = 0
            for line in rec.order_line:
                toplam += line.birim_kar * line.product_uom_qty
            rec.margin = toplam
            if (rec.amount_untaxed - toplam) > 0:
                rec.margin_percent = (toplam) / (rec.amount_untaxed - toplam)
            else:
                rec.margin_percent = 100
