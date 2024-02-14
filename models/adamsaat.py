# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    adamsaat = fields.Float (string = "Adam/Saat", default = 0.0, digits=(12,3) )
    liste_fiyat = fields.Float(string = "Liste Fiyatı",  store=True)



class SaleOrder(models.Model):
    _inherit = "sale.order"

    toplam_adamsaat = fields.Float("toplam Adam/Saat", compute='_compute_toplam_adamsaat', store=True)
    adamsaat_maliyet = fields.Float("Adam/Saat Fiyat", default="7")
    malzeme_margin = fields.Float("Malzeme Marj", compute='_compute_malzeme_marj', store=True)
    malzeme_maliyet = fields.Float("Malzeme Maliyet", compute='_compute_malzeme_maliyet', store=True)



    @api.depends('margin', 'toplam_adamsaat')
    def _compute_malzeme_marj(self):
        """
        Compute the amounts of the SO line.
        """
        for rec in self:
            toplam = 0
            for line in rec.order_line:
                if line.product_template_id.detailed_type != "service":
                    toplam += line.product_uom_qty * line.birim_kar
            rec.malzeme_margin = toplam

    @api.depends('margin', 'toplam_adamsaat')
    def _compute_malzeme_maliyet(self):
        """
        Compute the amounts of the SO line.
        """
        for rec in self:
            toplam = 0
            for line in rec.order_line:
                if line.product_template_id.detailed_type != "service":
                    toplam += line.product_uom_qty * line.purchase_price
            rec.malzeme_maliyet = toplam



    @api.depends('order_line', 'order_line.adamsaat', 'adamsaat_maliyet')
    def _compute_toplam_adamsaat(self):
        """
        Compute the amounts of the SO line.
        """
        for rec in self:
            toplam = 0
            for line in rec.order_line:
                toplam += line.adamsaat_subtotal
            rec.toplam_adamsaat = toplam * rec.adamsaat_maliyet





class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    adamsaat = fields.Float(related='product_id.adamsaat', depends=['product_id'])


    adamsaat_subtotal = fields.Float(
        string="adamsaat toplam",
        compute='_compute_adamsaat',
        store=True, precompute=True)


    @api.depends('product_uom_qty', 'adamsaat')
    def _compute_adamsaat(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            line.adamsaat_subtotal = line.product_uom_qty * line.adamsaat * self.order_id.adamsaat_maliyet		
