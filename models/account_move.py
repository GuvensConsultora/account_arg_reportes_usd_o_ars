from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_factura_dolares = fields.Boolean(string="Factura en USD")
    x_tipo_cambio = fields.Float(string="Tipo de cambio", digits=(12, 4))

class SaleMove(models.Model):
    _inherit = 'sale.order'

    x_sale_dolares = fields.Boolean(string="Cotización en USD")
    x_tipo_cambio = fields.Float(string="Tipo de cambio", digits=(12, 4))


class SalelineMove(models.Model):
    _inherit = 'sale.order.line'

    x_sale_pcio_usd = fields.Float(string="Pcio Usd", digits=(12, 4))

    @api.onchange('x_sale_pcio_usd', 'order_id.x_tipo_cambio', 'order_id.x_sale_dolares')
    def _onchange_price_usd(self):
        #raise UserError(f"El precio unitario ha sido calculado como {self.price_unit}.")
        for line in self:
            if (
                    self.order_id.x_sale_dolares and
                    self.x_sale_pcio_usd and
                    self.order_id.x_tipo_cambio
            ):
                self.price_unit = self.x_sale_pcio_usd * self.order_id.x_tipo_cambio              
    # Hay que mejorar este código
    @api.onchange('x_sale_pcio_usd', 'order_id.x_tipo_cambio')
    def _onchange_price_usd(self):
        if self.order_id.x_tipo_cambio and self.x_sale_pcio_usd:
            self.price_unit = self.x_sale_pcio_usd * self.order_id.x_tipo_cambio
