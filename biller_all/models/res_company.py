# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _inherit = 'res.company'

    access_token = fields.Char("Token de acceso Biller")
    
    branch_office = fields.Integer("Sucursal ID Biller")

    biller_default_product_id = fields.Many2one(
        comodel_name='product.product',
        string="Producto por defecto",
        help="Producto por defecto a usar para crear comprobantes recibidos por Biller",
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
