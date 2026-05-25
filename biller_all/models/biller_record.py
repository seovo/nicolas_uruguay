# -*- encoding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields
from odoo.exceptions import UserError, ValidationError
import http.client
from base64 import b64decode
import fitz

# If you are here, I'm truly sorry for you. 

ENV = 'prod'
class BillerRecord(models.Model):
    _name = 'biller.record'
    _description = "Model to keep track of sent and received biller messages"
    
    document_type = fields.Selection([
        ('cfe_sent', 'Factura Enviada'),
        ('cfe_received', 'Factura Recibida'),
        ('payment_sent', 'Pago enviado'),
        ('payment_canceled', 'Pago cancelado'),], 
        readonly=True,
        string = "Tipo de documento"
    )

    name = fields.Char("Documento Origen", copy=False,readonly=True)

    payload = fields.Text("Payload", copy=False,readonly=True)

    response = fields.Text("Respuesta", copy=False,readonly=True)

    response_date = fields.Datetime("Fecha de creación", copy=False,readonly=True)

    def get_response(self, type, request_string, payload):
        conn = BillerRecord.get_biller_url()
        authorization = 'Bearer {}'.format(self.env.company.access_token)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': authorization
        }
        conn.request(type, request_string, payload, headers)
        return conn.getresponse()

    def post_document(self, payload, type):
        res = self.get_response("POST","/v2/comprobantes/crear",payload)
        data = res.read()
        self.create({
            'name' : eval(data.decode())["serie"] + "-" + str(eval(data.decode())["numero"]) if res.code == 201 else "Error",
            'document_type' : type,
            'payload' : payload,
            'response' : data,
            'response_date' : datetime.now()
        })
        self.env.cr.commit()
        return res, data

    def get_sent_documents(self, doc_id, branch_office, date_from, date_to):
        doc_id = ("id=" + str(doc_id)+ "&") if doc_id else ''
        branch_office = ("sucursal=" + str(branch_office) + "&") if branch_office else ''
        date_from = date_from.strftime("%Y-%m-%d") if date_from else fields.Date.today().strftime("%Y-%m-%d")
        date_to = date_to.strftime("%Y-%m-%d") if date_to else fields.Date.today().strftime("%Y-%m-%d")
        request_string = "/v2/comprobantes/obtener?{}{}desde={}%2000:00:00&hasta={}%2023:59:59".format(doc_id, branch_office, date_from, date_to)
        payload = ''
        res = self.get_response("GET", request_string, payload)
        data = res.read()    
        return self.create({
            'name' : "Obtener comprobantes {}".format(datetime.now().strftime("%d/%m/%Y %H:%M")),
            'document_type' : 'cfe_received',
            'payload' : payload,
            'response' : data if bool(data) else "No hubo comprobantes en el rango especificado de {} a {}".format(date_from, date_to),
            'response_date' : fields.Date.today()
        })

    def get_received_documents(self, date_from, date_to):
        date_from = date_from.strftime("%Y-%m-%d") if date_from else fields.Date.today().strftime("%Y-%m-%d")
        date_to = date_to.strftime("%Y-%m-%d") if date_to else (fields.Date.today()).strftime("%Y-%m-%d")
        request_string = "/v2/comprobantes/obtener?recibidos=1&desde={}%2000:00:00&hasta={}%2023:59:59".format(date_from, date_to)
        payload = ''
        res = self.get_response("GET", request_string, payload)
        data = res.read()
        self.create({
            'name' : "Obtener comprobantes {}".format(datetime.now().strftime("%d/%m/%Y %H:%M")),
            'document_type' : 'cfe_received',
            'payload' : payload,
            'response' : data if bool(data) else "No hubo comprobantes en el rango especificado de {} a {}".format(date_from, date_to),
            'response_date' : fields.Date.today()
        })
        return data

    def get_received_documents_dgi(self, date_from, date_to):
        date_from = date_from.strftime("%Y-%m-%d") if date_from else (fields.Date.today()).strftime("%Y-%m-%d")
        date_to = date_to.strftime("%Y-%m-%d") if date_to else (fields.Date.today()).strftime("%Y-%m-%d")
        request_string = "/v2/comprobantes/recibidos/obtener?fecha_desde={}&fecha_hasta={}".format(date_from, date_to)
        payload = ''
        res = self.get_response("GET", request_string, payload)
        data = res.read()
        self.create({
            'name' : "Obtener comprobantes DGI{}".format(datetime.now().strftime("%d/%m/%Y %H:%M")),
            'document_type' : 'cfe_received',
            'payload' : payload,
            'response' : data if bool(data) else "No hubo comprobantes en el rango especificado de {} a {}".format(date_from, date_to),
            'response_date' : fields.Date.today()
        })
        return data

    def get_biller_pdf(self, biller_id, token):
        conn = BillerRecord.get_biller_url()
        payload = ''
        authorization = 'Bearer {}'.format(token)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': authorization
        }
        conn.request("GET", "/v2/comprobantes/pdf?id={}".format(biller_id), payload, headers)
        res = conn.getresponse()
        data = res.read()
        bytes = b64decode(data.decode())
        doc = fitz.open("pdf", bytes)
        blocks = []
        i=0
        for page in doc:
            page_blocks = page.get_text("blocks", sort=True)
            if i > 0:
                page_blocks = page_blocks[5:]
            blocks+= page_blocks[:len(page_blocks)-3]
            i+=1
        return data, blocks

    def cancel(self, request_string, payload, type):
        res = self.get_response("POST", request_string, payload)
        data = res.read()
        self.create({
            'name': eval(data.decode())["serie"] + "-" + str(eval(data.decode())["numero"]) if res.code == 201 else "Error on {} action".format(type),
            'document_type': type,
            'payload': payload,
            'response': data,
            'response_date': datetime.now()
        })
        self.env.cr.commit()
        return res, data
    
    @staticmethod
    def get_biller_url():
        if ENV == 'prod':
            return http.client.HTTPSConnection("biller.uy")
        else:
            return http.client.HTTPSConnection("test.biller.uy")
        
    def get_document_by_internal_number(self, internal_number):
        request_string = "/v2/comprobantes/obtener?numero_interno={}".format(internal_number)
        payload = ''
        res = self.get_response("GET", request_string, payload)
        data = res.read()
        self.create({
            'name' : eval(data.decode())["serie"] + "-" + str(eval(data.decode())["numero"]) if res.code == 201 else "Error",
            'payload' : payload,
            'response' : data,
            'response_date' : datetime.now()
        })
        return res, data
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
