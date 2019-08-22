# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class AccountAbstractAnalyticContractLine(models.AbstractModel):
    _inherit = 'contract.abstract.line'

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id.is_contract:
            self.recurring_rule_type = self.product_id.recurring_rule_type
            self.recurring_invoicing_type = (
                self.product_id.recurring_invoicing_type
            )
            self.recurring_interval = self.product_id.recurring_interval
            self.date_start = fields.Date.today()
