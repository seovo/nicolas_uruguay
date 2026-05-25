# -*- encoding: utf-8 -*-
from odoo import models, fields
import json
from datetime import datetime

CODES = {
    111 : "account.move",
    101 : "account.move"
}
class GetDocumentsWizard(models.TransientModel):

    _name = 'get.documents.wizard'

    document_id = fields.Integer("ID del CFE")

    branch_office_id = fields.Integer("ID de la Sucurusal Emisora")

    date_from = fields.Date("Fecha creación desde")
    
    date_to = fields.Date("Fecha creación hasta")

    def manual_get_sent_documents(self):
        biller_proxy = self.env['biller.record']
        res = biller_proxy.get_documents(self.document_id, self.branch_office_id, self.date_from, self.date_to)
        return {
            'name': 'Documentos emitidos',
            'res_model': 'biller.record',
            'type': 'ir.actions.act_window',
            'domain': [('id', '=', res.id)],
            'views': [[False, "tree"], [False, "form"]],
        }

    def manual_create_received_documents(self):
        biller_proxy = self.env['biller.record']
        res = biller_proxy.get_received_documents(self.date_from, self.date_to)
        data = res.decode()
        records =  json.loads(data)
        self.record_maker(records)
        res = biller_proxy.get_received_documents_dgi(self.date_from, self.date_to)
        data = res.decode()
        records =  json.loads(data)
        self.record_maker_dgi(records)
        return

    def record_maker(self, records):
        for rec in records:
            try:
                model = CODES[rec["tipo_comprobante"]]
                self.env[model].create_received(rec)
            except KeyError:
                continue
        return

    def record_maker_dgi(self, records):
        for rec in records:
            try:
                model = CODES[rec["tipo"]]
                self.env[model].create_received_dgi(rec)
            except KeyError:
                continue
        return

    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
