# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    cash = fields.Boolean(string="Cash",translate=True)
    cash_account_id = fields.Many2one('account.account',string="Cash Account",translate=True)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):
        super(AccountInvoice, self)._onchange_payment_term_date_invoice()
        if self.payment_term_id.cash:
            self.account_id = self.payment_term_id.cash_account_id.id
