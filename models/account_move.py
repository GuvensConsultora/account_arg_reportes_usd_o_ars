from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_factura_dolares = fields.Boolean(string="Factura en USD")
    x_tipo_cambio = fields.Float(string="Tipo de cambio", digits=(12, 4))

    # Por qué: campo Json compute para precalcular importes USD y evitar
    # errores de redondeo al dividir cada línea por separado en QWeb.
    # Patrón: Single Source of Truth — el total se convierte UNA vez
    # y la diferencia de redondeo se ajusta en la última línea.
    # Tip: fields.Json devuelve dict nativo → se accede directo en QWeb
    # sin necesitar json.loads() (que no está en el contexto QWeb).
    x_usd_display_data = fields.Json(
        string="USD Display Data",
        compute="_compute_usd_values",
    )

    @api.depends(
        'x_factura_dolares', 'x_tipo_cambio',
        'invoice_line_ids.price_unit', 'invoice_line_ids.price_subtotal',
        'amount_untaxed', 'amount_total', 'tax_totals',
    )
    def _compute_usd_values(self):
        """Calcula importes USD exactos. La suma de líneas == total.

        Por qué: cada round() individual acumula error de centavos.
        Con 5-10 líneas la diferencia puede ser significativa.
        Solución: convertir total una sola vez (fuente de verdad)
        y ajustar la diferencia en la última línea.
        """
        for move in self:
            if not (move.x_factura_dolares and move.x_tipo_cambio):
                move.x_usd_display_data = False
                continue

            tc = move.x_tipo_cambio

            # --- Líneas de factura ---
            lines_usd = []
            sum_lines = 0.0

            for line in move.invoice_line_ids.filtered(
                lambda l: not l.display_type
            ):
                price_unit_usd = round(line.price_unit / tc, 2)
                price_subtotal_usd = round(line.price_subtotal / tc, 2)
                # Por qué: line.id puede ser NewId en borrador → convertir a int
                # para garantizar serialización JSON. Si no tiene id real, usar 0.
                line_id = line.id if isinstance(line.id, int) else 0
                lines_usd.append({
                    'line_id': line_id,
                    'price_unit_usd': price_unit_usd,
                    'price_subtotal_usd': price_subtotal_usd,
                })
                sum_lines += price_subtotal_usd

            # Total convertido una sola vez (fuente de verdad)
            subtotal_usd = round(move.amount_untaxed / tc, 2)
            total_usd = round(move.amount_total / tc, 2)

            # Tip: ajustar diferencia en última línea para que
            # suma de líneas == subtotal exacto
            diff = round(subtotal_usd - sum_lines, 2)
            if lines_usd and diff != 0:
                lines_usd[-1]['price_subtotal_usd'] = round(
                    lines_usd[-1]['price_subtotal_usd'] + diff, 2
                )

            # --- Impuestos ---
            taxes_usd = []
            sum_taxes = 0.0
            tax_totals = move.tax_totals or {}
            groups = tax_totals.get(
                'groups_by_subtotal', {}
            ).get('Subtotal', [])

            for group in groups:
                tax_amount_usd = round(
                    group['tax_group_amount'] / tc, 2
                )
                tax_base_usd = round(
                    group['tax_group_base_amount'] / tc, 2
                )
                taxes_usd.append({
                    'name': group['tax_group_name'],
                    'amount_usd': tax_amount_usd,
                    'base_usd': tax_base_usd,
                    'hide_base_amount': group.get('hide_base_amount', False),
                })
                sum_taxes += tax_amount_usd

            # Verificar subtotal + impuestos == total
            # Si hay diff por redondeo, ajustar en último impuesto
            expected_tax_total = round(total_usd - subtotal_usd, 2)
            tax_diff = round(expected_tax_total - sum_taxes, 2)
            if taxes_usd and tax_diff != 0:
                taxes_usd[-1]['amount_usd'] = round(
                    taxes_usd[-1]['amount_usd'] + tax_diff, 2
                )

            # fields.Json acepta dict nativo, no necesita json.dumps()
            move.x_usd_display_data = {
                'lines': lines_usd,
                'subtotal_usd': subtotal_usd,
                'total_usd': total_usd,
                'taxes': taxes_usd,
                'tipo_cambio': tc,
            }


class SaleMove(models.Model):
    _inherit = 'sale.order'

    x_sale_dolares = fields.Boolean(string="Cotización en USD")
    x_tipo_cambio = fields.Float(string="Tipo de cambio", digits=(12, 4))


class SalelineMove(models.Model):
    _inherit = 'sale.order.line'

    x_sale_pcio_usd = fields.Float(string="Pcio Usd", digits=(12, 4))

    @api.onchange('x_sale_pcio_usd', 'order_id.x_tipo_cambio')
    def _onchange_price_usd(self):
        # Por qué: convierte precio USD a ARS usando TC manual
        if self.order_id.x_tipo_cambio and self.x_sale_pcio_usd:
            self.price_unit = self.x_sale_pcio_usd * self.order_id.x_tipo_cambio
