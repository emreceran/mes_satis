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



class kredikart(models.Model):
    _name = 'mes_satis.kredi_kart'
    _description = 'Kredi kartı'

    name = fields.Char(string='Kredi Kartı', required=True, translate=True)

    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()
    #
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100



class ProductTemplate(models.Model):
    _inherit = "hr.expense"

    kredi_kart_id = fields.Many2one('mes_satis.kredi_kart',"Kredi Kartı" )

