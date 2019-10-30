# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    automatic_invoice_validation = fields.Boolean(
        help=("If this is activated, all recurring invoices created by this "
              "contract will be automatically validated."))
    send_by_mail = fields.Boolean(
        string="Send Automatic Email",
        help=("If this is activated, all reccuring invoices created by this "
              "contract will be send by mail upon validation."))

    def _create_invoice(self):
        invoice = super(AccountAnalyticAccount, self)._create_invoice()
        if self.automatic_invoice_validation:
            # Avoid failure when the  cron is doing its job.
            # The validation could fail for multiple reasons (chronology
            # problem for instance)
            try:
                invoice.action_invoice_open()
                # TODO send mail
            except Exception as e:
                if self.env.context.get('cron'):
                    pass
                else:
                    raise e

