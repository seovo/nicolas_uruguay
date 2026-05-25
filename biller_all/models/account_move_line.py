# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    invoicing_indicator = fields.Selection([
        ('1', 'Exento de IVA'),
        ('2', 'Tasa mínima'),
        ('3', 'Tasa básica'),
        ('4', 'Otra tasa'),
        ('5', 'Entrega gratuita'),
        ('6', 'Producto o servicio no facturable'),
        ('7', 'Producto o servicio no facturable negativo'),
        ('8', 'Ítem a rebajar en e-remitos y en e-remitos de exportación'),
        ('9', 'Ítem a anular en resguardos'),
        ('10', 'Exportación y asimiladas'),
        ('11', 'Impuesto percibido'),
        ('12', 'IVA en suspenso'),
        ('13', 'Ítem vendido no contribuyente'),
        ('14', 'Ítem vendido contribuyente monotributo'),
        ('15', 'Ítem vendido contribuyente IMEBA'),], 
        string = "Indicador Facturacion",
        default = '3'
    )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
