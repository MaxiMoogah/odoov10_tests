from odoo import http, models, fields, api, _
from cStringIO import StringIO
import base64
import xlwt

class CustomerOutstandingStatementWizard2(models.TransientModel):
    _name = "customer.outstanding.statement.wizard2"
    _inherit = "customer.outstanding.statement.wizard"

    type = fields.Selection([('customer','customer'),('supplier','supplier')])
    print_by = fields.Selection([('html','HTML'),('pdf','PDF'),('excel','Export xlsx')],
                                string="Printing Options",default="html",required=True)
    number_partner_ids = fields.Integer(default=0)
    c_partner_ids = fields.Many2many('res.partner', string="Customers", translate=True, domain="[('customer', '=', True)]")
    p_partner_ids = fields.Many2many('res.partner', string="Suppliers", translate=True, domain="[('supplier', '=', True)]")


    def doit(self):
        if self.type == 'customer':
            ids = self.c_partner_ids._ids
            if not ids:
                ids = self.env['res.partner'].search([('customer', '=', True)])._ids
        if self.type == 'supplier':
            ids = self.p_partner_ids._ids
            if not ids:
                ids = self.env['res.partner'].search([('supplier', '=', True)])._ids

        datas = {
            'date_end': self.date_end,
            'company_id': self.company_id.id,
            'partner_ids': ids,
            'show_aging_buckets': self.show_aging_buckets,
            'filter_non_due_partners': self.filter_partners_non_due,
            'docs': ids,
        }
        if self.print_by in ('html','pdf'):
            if self.print_by == 'pdf':
                return self.env['report'].with_context(landscape=True).get_action(self,'customer_outstanding_statement.statement', data=datas)
            if self.print_by == 'html':
                return self.env['report'].with_context(landscape=True).get_action(self,'vitt_customer_outstanding_statement.statement', data=datas)

        if self.print_by == 'excel':
            data = datas
            company_id = data['company_id']
            partner_ids = data['partner_ids']
            date_end = data['date_end']
            today = fields.Date.today()

            buckets_to_display = {}
            lines_to_display, amount_due = {}, {}
            currency_to_display = {}
            today_display, date_end_display = {}, {}

            rep_obj = self.env['report.customer_outstanding_statement.statement']
            lines = rep_obj._get_account_display_lines(
                company_id, partner_ids, date_end)

            for partner_id in partner_ids:
                lines_to_display[partner_id], amount_due[partner_id] = {}, {}
                currency_to_display[partner_id] = {}
                today_display[partner_id] = rep_obj._format_date_to_partner_lang(
                    today, partner_id)
                date_end_display[partner_id] = rep_obj._format_date_to_partner_lang(
                    date_end, partner_id)
                for line in lines[partner_id]:
                    currency = self.env['res.currency'].browse(line['currency_id'])
                    if currency not in lines_to_display[partner_id]:
                        lines_to_display[partner_id][currency] = []
                        currency_to_display[partner_id][currency] = currency
                        amount_due[partner_id][currency] = 0.0
                    if not line['blocked']:
                        amount_due[partner_id][currency] += line['open_amount']
                    line['balance'] = amount_due[partner_id][currency]
                    line['date'] = rep_obj._format_date_to_partner_lang(line['date'], partner_id)
                    line['date_maturity'] = rep_obj._format_date_to_partner_lang(line['date_maturity'], partner_id)

                    # NEW
                    move = self.env['account.move'].search([('name', '=', line['move_id'])])
                    if move.origin_document:
                        line['move_id'] = move.origin_document

                    lines_to_display[partner_id][currency].append(line)

            if data['show_aging_buckets']:
                buckets = rep_obj._get_account_show_buckets(
                    company_id, partner_ids, date_end)
                for partner_id in partner_ids:
                    buckets_to_display[partner_id] = {}
                    for line in buckets[partner_id]:
                        currency = self.env['res.currency'].browse(
                            line['currency_id'])
                        if currency not in buckets_to_display[partner_id]:
                            buckets_to_display[partner_id][currency] = []
                        buckets_to_display[partner_id][currency] = line

            docargs = {
                'doc_ids': partner_ids,
                'doc_model': 'res.partner',
                'docs': self.env['res.partner'].browse(partner_ids),
                'Amount_Due': amount_due,
                'Lines': lines_to_display,
                'Buckets': buckets_to_display,
                'Currencies': currency_to_display,
                'Show_Buckets': data['show_aging_buckets'],
                'Filter_non_due_partners': data['filter_non_due_partners'],
                'Date_end': date_end_display,
                'Date': today_display,
            }

            context = self._context
            filename = 'Outstanding_report.xls'
            workbook = xlwt.Workbook(encoding="UTF-8")
            worksheet = workbook.add_sheet('Detalle')
            line = row = 0
            for partner in docargs['docs']:
                if len(docargs['Lines'][partner.id]) > 0:
                    worksheet.write(line, row, _('Partner'))
                    row += 1
                    worksheet.write(line, row, partner.name)


                    for currency in docargs['Lines'][partner.id]:
                        line += 1
                        row = 0
                        worksheet.write(line, row, _('Reference number'))
                        row += 1
                        worksheet.write(line, row, _('Date'))
                        row += 1
                        worksheet.write(line, row, _('Due Date'))
                        row += 1
                        worksheet.write(line, row, _('Description'))
                        row += 1
                        worksheet.write(line, row, _('Original Amount'))
                        row += 1
                        worksheet.write(line, row, _('Open Amount'))
                        row += 1
                        worksheet.write(line, row, _('Balance'))
                        line += 1
                        row = 0
                        for line_doc in docargs['Lines'][partner.id][currency]:
                            worksheet.write(line, row, line_doc['move_id'])
                            row += 1
                            worksheet.write(line, row, line_doc['date'])
                            row += 1
                            worksheet.write(line, row, line_doc['date_maturity'])
                            row += 1
                            tmp = ""
                            if line_doc['name'] != '/':
                                if not line_doc['ref']:
                                    tmp = line_doc['name']
                                if line_doc['name'] and line_doc['ref']:
                                    if line_doc['name'] not in line_doc['ref']:
                                        tmp = line_doc['name']
                                    if line_doc['ref'] not in line_doc['name']:
                                        tmp = line_doc['ref']
                            else:
                                tmp = line_doc['ref']
                            worksheet.write(line, row, tmp)
                            row += 1
                            worksheet.write(line, row, line_doc['amount'])
                            row += 1
                            worksheet.write(line, row, line_doc['open_amount'])
                            row += 1
                            worksheet.write(line, row, line_doc['balance'])
                            row = 0
                            line += 1
                        line += 2
                        row = 0
                        worksheet.write(line, row, _('aging report at ') + docargs['Date_end'][partner.id] + ' in '
                                        + docargs['Currencies'][partner.id][currency].name)
                        line += 1
                        row  = 0
                        worksheet.write(line, row, _('Current Due'))
                        row  += 1
                        worksheet.write(line, row, _('1-30 Days Due'))
                        row  += 1
                        worksheet.write(line, row, _('30-60 Days Due'))
                        row  += 1
                        worksheet.write(line, row, _('60-90 Days Due'))
                        row  += 1
                        worksheet.write(line, row, _('90-120 Days Due'))
                        row  += 1
                        worksheet.write(line, row, _('+120 Days Due'))
                        row  += 1
                        worksheet.write(line, row, _('Balance'))

                        line += 1
                        row = 0
                        worksheet.write(line, row, docargs['Buckets'][partner.id][currency]['current'])
                        row  += 1
                        worksheet.write(line, row, docargs['Buckets'][partner.id][currency]['b_1_30'])
                        row  += 1
                        worksheet.write(line, row, docargs['Buckets'][partner.id][currency]['b_30_60'])
                        row  += 1
                        worksheet.write(line, row, docargs['Buckets'][partner.id][currency]['b_60_90'])
                        row  += 1
                        worksheet.write(line, row, docargs['Buckets'][partner.id][currency]['b_90_120'])
                        row  += 1
                        worksheet.write(line, row, docargs['Buckets'][partner.id][currency]['b_over_120'])
                        row  += 1
                        worksheet.write(line, row, docargs['Buckets'][partner.id][currency]['balance'])
                        line += 2
                        row = 0



            fp = StringIO()
            workbook.save(fp)
            export_id = self.env['excel.extended'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename }).id
            fp.close()
            return{
                'view_mode': 'form',
                'res_id': export_id,
                'res_model': 'excel.extended',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'context': context,
                'target': 'new',
            }





class CustomerOutstandingStatement(models.AbstractModel):
    _name = 'report.vitt_customer_outstanding_statement.statement'
    _inherit = 'report.customer_outstanding_statement.statement'

class CustomerOutstandingStatement2(models.AbstractModel):
    """Model of Customer Outstanding Statement"""

    _inherit = 'report.customer_outstanding_statement.statement'

    @api.multi
    def render_html(self, docids, data):
        company_id = data['company_id']
        partner_ids = data['partner_ids']
        date_end = data['date_end']
        today = fields.Date.today()

        buckets_to_display = {}
        lines_to_display, amount_due = {}, {}
        currency_to_display = {}
        today_display, date_end_display = {}, {}

        lines = self._get_account_display_lines(
            company_id, partner_ids, date_end)

        for partner_id in partner_ids:
            lines_to_display[partner_id], amount_due[partner_id] = {}, {}
            currency_to_display[partner_id] = {}
            today_display[partner_id] = self._format_date_to_partner_lang(
                today, partner_id)
            date_end_display[partner_id] = self._format_date_to_partner_lang(
                date_end, partner_id)
            for line in lines[partner_id]:
                currency = self.env['res.currency'].browse(line['currency_id'])
                if currency not in lines_to_display[partner_id]:
                    lines_to_display[partner_id][currency] = []
                    currency_to_display[partner_id][currency] = currency
                    amount_due[partner_id][currency] = 0.0
                if not line['blocked']:
                    amount_due[partner_id][currency] += line['open_amount']
                line['balance'] = amount_due[partner_id][currency]
                line['date'] = self._format_date_to_partner_lang(line['date'], partner_id)
                line['date_maturity'] = self._format_date_to_partner_lang(line['date_maturity'], partner_id)

                #NEW
                move = self.env['account.move'].search([('name', '=', line['move_id'])])
                if move.origin_document:
                        line['move_id'] = move.origin_document


                lines_to_display[partner_id][currency].append(line)

        if data['show_aging_buckets']:
            buckets = self._get_account_show_buckets(
                company_id, partner_ids, date_end)
            for partner_id in partner_ids:
                buckets_to_display[partner_id] = {}
                for line in buckets[partner_id]:
                    currency = self.env['res.currency'].browse(
                        line['currency_id'])
                    if currency not in buckets_to_display[partner_id]:
                        buckets_to_display[partner_id][currency] = []
                    buckets_to_display[partner_id][currency] = line

        docargs = {
            'doc_ids': partner_ids,
            'doc_model': 'res.partner',
            'docs': self.env['res.partner'].browse(partner_ids),
            'Amount_Due': amount_due,
            'Lines': lines_to_display,
            'Buckets': buckets_to_display,
            'Currencies': currency_to_display,
            'Show_Buckets': data['show_aging_buckets'],
            'Filter_non_due_partners': data['filter_non_due_partners'],
            'Date_end': date_end_display,
            'Date': today_display,
        }
        return self.env['report'].render(
            'customer_outstanding_statement.statement', values=docargs)
