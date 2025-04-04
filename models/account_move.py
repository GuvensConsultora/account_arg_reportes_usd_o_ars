from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_factura_dolares = fields.Boolean(string="Factura en USD")
    x_tipo_cambio = fields.Float(string="Tipo de cambio", digits=(12, 4))
