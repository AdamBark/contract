# Copyright 2021 Akretion - Kevin Roche
# Copyright 2021 Akretion - Raphaël Reverdy
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AbstractContractLine(models.AbstractModel):
    _inherit = ["contract.abstract.contract.line", "product.secondary.unit.mixin"]
    _name = "contract.abstract.contract.line"
    _secondary_unit_fields = {
        "qty_field": "quantity",
        "uom_field": "uom_id",
    }

    secondary_uom_qty = fields.Float(string="2nd Qty", digits="Product Unit of Measure")
    secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="2nd uom",
        ondelete="restrict",
    )
    quantity = fields.Float(
        store=True, readonly=False, compute="_compute_quantity", copy=True
    )

    secondary_uom_unit_price = fields.Float(
        string="2nd unit price",
        digits="Product Unit of Measure",
        store=False,
        readonly=True,
        compute="_compute_secondary_uom_unit_price",
    )

    @api.depends("secondary_uom_qty", "secondary_uom_id", "quantity", "uom_id")
    def _compute_quantity(self):
        self._compute_helper_target_field_qty()

    @api.onchange("uom_id")
    def onchange_product_uom_for_secondary(self):
        self._onchange_helper_product_uom_for_secondary()

    @api.depends("secondary_uom_qty", "quantity", "price_unit")
    def _compute_secondary_uom_unit_price(self):
        for line in self:
            if line.secondary_uom_id:
                line.secondary_uom_unit_price = (
                    line.price_subtotal / line.secondary_uom_qty
                )
            else:
                line.secondary_uom_unit_price = 0
