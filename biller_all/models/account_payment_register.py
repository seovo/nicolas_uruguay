# -*- encoding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
import json

class AccountPaymentRegister(models.TransientModel):

    _inherit = 'account.payment.register'

    def action_create_payments(self):
        payments = self._create_payments()

        original_move = self.env['account.move'].browse(self.env.context['active_ids']) # Esto esta feo, mejorar en algun momento
        if original_move.partner_id.vat != '-':
            payload = json.dumps(self.get_payload())
            biller_proxy = self.env['biller.record']
            request_string = "/v2/recibos/crear"
            response = biller_proxy.get_response("POST", request_string, payload)
            data = response.read()
            biller_proxy.create({
                'name': eval(data.decode())["serie"] + "-" + str(eval(data.decode())["numero"]) if response.code == 201 else "Error",
                'document_type': 'cfe_sent',
                'payload': payload,
                'response': data,
                'response_date': datetime.now()
            })
            self.env.cr.commit()
            if response.code != 201:
                raise ValidationError("Hubo problemas al enviar el pago.")

            for payment in payments:
                payment.biller_id = eval(data.decode())["id"]
                original_move.payment_id = payment.id

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })

        return action

    def get_payload(self,):
        original_move = self.env['account.move'].browse(self.env.context['active_ids'])
        payload = original_move.get_payload()
        payload["referencias"] = [{
                    "padre": original_move.biller_id,
                    "total": self.amount
                },]
        payload["pago"] = {
                "fecha": self.payment_date.strftime("%d/%m/%Y"),
                "monto": self.amount,
                "referencia": self.communication
        }
        return payload


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
