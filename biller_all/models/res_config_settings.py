# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    biller_default_product_id = fields.Many2one(
        related="company_id.biller_default_product_id",
        readonly=False
    )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
