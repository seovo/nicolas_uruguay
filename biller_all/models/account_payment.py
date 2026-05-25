# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    biller_id = fields.Integer("ID Biller",readonly=True,copy=False)

    def biller_cancel_self(self):
        biller_proxy = self.env['biller.record']
        request_string = "/v2/recibos/cancelar/{}".format(self.biller_id)
        payload = ""
        res, data = biller_proxy.cancel(request_string, payload, "payment_canceled")
        if not (res.code == 201 or res.code == 400): 
            raise ValidationError("Hubo problemas al cancelar el pago")
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
