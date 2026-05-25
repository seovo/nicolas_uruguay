# -*- encoding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_discount = fields.Boolean("Es descuento o recargo")

    discount_overcharge = fields.Selection([
            ('discount', 'Descuento'), 
            ('overcharge', 'Recargo')],
            string = "Recargo/Descuento"
            )

    min_rate_tax = fields.Many2one(
        comodel_name='account.tax',
        string="Tasa basica",
        domain=[('type_tax_use', '=', 'purchase')], 
        default=lambda self: self.env.company.account_purchase_tax_id
    )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
