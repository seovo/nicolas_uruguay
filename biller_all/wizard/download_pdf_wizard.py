# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import base64
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition

class DownloadPdfWizard(models.TransientModel):

    _name = 'download.pdf.wizard'

    def print_biller_pdf(self, biller_id, name, token):
        filename = "{}.pdf".format(name)
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_account_move_biller_report?biller_id=%s&filename=%s&token=%s' % (biller_id, filename, token),
            'target': 'new',
        }
    
class AccountMoveBillerReport(http.Controller):
    @http.route('/web/binary/download_account_move_biller_report', type='http', auth="public")
    def download_account_move_biller_report(self, debug=1, biller_id=0, filename='', token=''):
        """ Descarga un documento cuando se accede a la url especificada en http route.
        :param debug: Si esta o no en modo debug.
        :param int wizard_id: Id del modelo que contiene el documento.
        :param filename: Nombre del archivo.
        :returns: :class:`werkzeug.wrappers.Response`, descarga del archivo excel.
        """
        response, _ = request.env['biller.record'].get_biller_pdf(int(biller_id),token)
        filecontent = base64.b64decode( response or '')
        return request.make_response(filecontent, [('Content-Type', 'application/octet-stream'),
                                                   ('Content-Disposition', content_disposition(filename))])



    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
