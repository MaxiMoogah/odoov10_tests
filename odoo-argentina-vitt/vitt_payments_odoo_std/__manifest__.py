# -*- coding: utf-8 -*-
{
    'name': "Standard Odoo Payments & Receipts",
    'summary': """Standard registers for Payments, purchase and sales transactions, using Odoo standard payments instead of Payment Groups""",
    'description': """Standard registers for Payments, purchase and sales transactions, using Odoo standard payments instead of Payment Groups""",
    'author': "Moogah",
    'website': "http://www.Moogah.com",
    'category': 'Uncategorized',
    'version': '10.0.1.0.3',
    'depends': [
        'account_accountant',
        'account_payment_group_document',
        'account_payment_group'
    ],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'application': True,
}