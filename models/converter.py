# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    currency_id = fields.Many2one(
        'res.currency', 'Currency', compute='_compute_currency_id')

    cost_currency_id = fields.Many2one(
        'res.currency', 'Cost Currency', compute='_compute_cost_currency_id')



    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            # template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id
            template.currency_id = self.env["res.currency"].search([("id","=","1")])

    @api.depends_context('company')
    def _compute_cost_currency_id(self):
        self.cost_currency_id = self.env["res.currency"].search([("id","=","1")])


class SaleOrder(models.Model):
    _inherit = "sale.order"




    def  action_update_prices(self):
        self.ensure_one()

        self._recompute_prices()



        if self.pricelist_id:
            self.message_post(body=_(
                "Product prices have been recomputed according to pricelist %s.",
                self.pricelist_id._get_html_link(),
            ))



    def _recompute_prices(self):
        lines_to_recompute = self._get_update_prices_lines()
        lines_to_recompute.invalidate_recordset(['pricelist_item_id'])
        print(self.pricelist_id.currency_id)
        # lines_to_recompute._compute_price_unit()
        # lines_to_recompute._convert_std_price()
        for line in lines_to_recompute:
            print(line.std_price, line.currency_id)
        print("asa")
        # Special case: we want to overwrite the existing discount on _recompute_prices call
        # i.e. to make sure the discount is correctly reset
        # if pricelist discount_policy is different than when the price was first computed.
        lines_to_recompute.discount = 0.0
        lines_to_recompute._compute_discount()
        self.show_update_pricelist = False

    @api.onchange('currency_id')
    def onchange_currency(self):
        print("para birimi")
        # self.purchase_price = (1 - self.cost_discount/100) * self.purchase_price
        # print(self.purchase_price)
        # for line in self:
        #     line = line.with_company(line.company_id)
        #     x = line.std_price
        #     line.purchase_price = (1 - (line.cost_discount)) * x
        #     line.birim_kar = self.birim_kar
        #     print(line.purchase_price)







class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"



    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _convert_std_price(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.qty_invoiced > 0:
                continue
            if not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
                line.std_price = 0.0
            else:
                price = line.with_company(line.company_id)._compute_std_price()
                line.std_price = line.product_id._get_tax_included_unit_price(
                    line.company_id,
                    line.order_id.currency_id,
                    line.order_id.date_order,
                    'sale',
                    fiscal_position=line.order_id.fiscal_position_id,
                    product_price_unit=price,
                    product_currency=line.currency_id
                )

    @api.onchange('currency_id')
    def onchange_std_price(self):
        # self.purchase_price = (1 - self.cost_discount/100) * self.purchase_price
        # print(self.purchase_price)
        for line in self:
            line = line.with_company(line.company_id)
            x = line.std_price
            line.purchase_price = (1 - (line.cost_discount)) * x
            line.birim_kar = self.birim_kar
            print(line.purchase_price)
