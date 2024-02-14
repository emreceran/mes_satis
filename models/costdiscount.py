# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    cost_discount = fields.Float("indirim", readonly=False, store=True, groups="base.group_user")


    std_price = fields.Float(
        string="Cost", compute="_compute_std_price",
        digits='Product Price', store=True, readonly=False, precompute=True,
        groups="base.group_user")

    purchase_price = fields.Float(
        string="Cost", compute="_compute_purchase_price",
        digits='Product Price', store=True, readonly=False, precompute=True,
        groups="base.group_user")

    birim_kar = fields.Float(
        string="Birim Kar", compute="_compute_birim_kar",
        digits='Birim Kar', store=True, readonly=False, precompute=True,
        groups="base.group_user")

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
    def _compute_std_price(self):
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            product_cost = line.product_id.liste_fiyat
            # line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)

            # product_cost = line.product_id.liste_fiyat
            # line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)
            # line.std_price = line.product_id.liste_fiyat
            line.std_price = line._convert_price(product_cost, line.product_id.uom_id,)


    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
    def _compute_birim_kar(self):
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            # product_cost = line.product_id.liste_fiyat
            # line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)

            # product_cost = line.product_id.liste_fiyat
            # line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)
            line.birim_kar = line.margin / line.product_uom_qty

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
    def _compute_purchase_price(self):
        # raise UserWarning(self.product_template_id.seller_ids.sorted(key = lambda s: s.price))
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            # product_cost = line.product_id.liste_fiyat
            # # line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)
            line.purchase_price = line.product_id.liste_fiyat

            # line = line.with_company(line.company_id)
            # product_cost = line.product_id.liste_fiyat
            # line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)

    def _convert_price(self, product_cost, from_uom):
        self.ensure_one()
        if not product_cost:
            # If the standard_price is 0
            # Avoid unnecessary computations
            # and currency conversions
            if not self.purchase_price:
                return product_cost
        from_currency = self.product_id.cost_currency_id
        to_cur = self.currency_id or self.order_id.currency_id
        # to_uom = self.product_uom
        # if to_uom and to_uom != from_uom:
        #     product_cost = from_uom._compute_price(
        #         product_cost,
        #         to_uom,
        #     )
        return from_currency._convert(
            from_amount=product_cost,
            to_currency=to_cur,
            company=self.company_id or self.env.company,
            date=self.order_id.date_order or fields.Date.today(),
            round=False,
        ) if to_cur and product_cost else product_cost
        # The pricelist may not have been set, therefore no conversion
        # is needed because we don't know the target currency..

    @api.onchange('cost_discount')
    def onchange_cost_discount(self):
        # self.purchase_price = (1 - self.cost_discount/100) * self.purchase_price
        # print(self.purchase_price)
        for line in self:
            line = line.with_company(line.company_id)
            product_cost = line.std_price
            x = product_cost
            # x = line._convert_price(product_cost, line.product_id.uom_id)
            line.purchase_price = (1 - (line.cost_discount)) * x
            line.margin = (line.price_subtotal * line.product_uom_qty) - (line.price_unit)
            print(line.purchase_price)


"""
@api.onchange('price_subtotal', 'margin_percent')
    def onchange_margin_percent(self):
        print("margin_percent")
        self.margin = self.price_subtotal - (self.purchase_price * self.product_uom_qty)
        self.birim_kar = self.margin / self.product_uom_qty
        if self._context.get('margin_percent'):
            self.margin_percent = self._context.get('margin_percent')
        if self.purchase_price > 0.0 and self.margin_percent and not self._context.get('get_sizes'):
            margin_percent = self.margin_percent
            montant_extras = self.purchase_price * (self.margin_percent)
            self.price_unit = self.purchase_price + self.birim_kar
            self.margin_percent = margin_percent
            context = dict(self.env.context)
            context.update({'get_sizes': True, 'margin_percent': margin_percent})
            self.env.context = context

    @api.onchange('margin')
    def onchange_margin(self):
        print("margin")
        if self.price_unit and not self._context.get('get_sizes') and not self._context.get('margin_percent'):
            self.price_unit = self.purchase_price + self.birim_kar

    @api.onchange('birim_kar')
    def onchange_birim_kar(self):
        print("birim_kar")
        # if self.price_unit and not self._context.get('get_sizes') and not self._context.get('margin_percent'):
        self.price_unit = self.purchase_price + self.birim_kar

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
    def _compute_std_price(self):
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue

            line = line.with_company(line.company_id)
            product_cost = line.product_id.liste_fiyat
            # from_currency = self.product_id.cost_currency_id
            # to_cur = self.currency_id or self.order_id.currency_id
            line.std_price = line._convert_price(product_cost, line.product_id.uom_id,)


    @api.depends('product_id', 'company_id', 'currency_id', 'purchase_price', 'margin_percent')
    def _compute_birim_kar(self):
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue


            line = line.with_company(line.company_id)
            line.birim_kar = line.purchase_price * line.margin_percent


    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
    def _compute_purchase_price(self):
        # raise UserWarning(self.product_template_id.seller_ids.sorted(key = lambda s: s.price))
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue

            if line.cost_discount ==0:
                line.purchase_price = line.std_price
            else:
                line.purchase_price =  (1 - (line.cost_discount)) * line.std_price

    # @api.depends('product_id', 'product_uom', 'purchase_price', 'birim_kar')
    # def _compute_price_unit(self):
    #     for line in self:
    #         # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
    #         # manually edited
    #         if line.qty_invoiced > 0:
    #             continue
    #         if not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
    #             line.price_unit = 0.0
    #         else:
    #             line.price_unit = line.purchase_price + line.birim_kar

    def _convert_price(self, product_cost, from_uom):
        self.ensure_one()
        if not product_cost:
            # If the standard_price is 0
            # Avoid unnecessary computations
            # and currency conversions
            if not self.purchase_price:
                return product_cost

        from_currency = self.product_id.cost_currency_id

        to_cur = self.currency_id or self.order_id.currency_id
        # to_uom = self.product_uom
        # if to_uom and to_uom != from_uom:
        #     product_cost = from_uom._compute_price(
        #         product_cost,
        #         to_uom,
        #     )
        return from_currency._convert(
            from_amount=product_cost,
            to_currency=to_cur,
            company=self.company_id or self.env.company,
            date=self.order_id.date_order or fields.Date.today(),
            round=False,
        ) if to_cur and product_cost else product_cost
        # The pricelist may not have been set, therefore no conversion
        # is needed because we don't know the target currency..


    @api.onchange('cost_discount')
    def onchange_cost_discount(self):
        # self.purchase_price = (1 - self.cost_discount/100) * self.purchase_price
        # print(self.purchase_price)
        for line in self:
            line = line.with_company(line.company_id)
            product_cost = line.std_price
            x = product_cost
            # x = line._convert_price(product_cost, line.product_id.uom_id)
            line.purchase_price = (1 - (line.cost_discount)) * x
            line.margin = (line.price_subtotal  * line.product_uom_qty) - (line.price_unit)
            print(line.purchase_price)


"""

