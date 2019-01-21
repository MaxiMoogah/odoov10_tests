# -*- coding: utf-8 -*-
{
    'name': "VITT App - Setting for Cash Invoice",
    'summary': """This app includes an account for the Payment Term to book the invoice to a Cash/Bank account instead of a Debtors one""",
    'description': """
        The app adds a new field to specify an account (type Bank or Cash) in order to book the invoice straight to this account instead of using the Debtors account. 
        The invoice will be marked as paid with no open value.
    """,
    'author': "Moogah",
    'website': "http://www.Moogah.com",
    'category': 'Uncategorized',
    'version': '10.0.1.0.1',
    'depends': [
        'account',
     ],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'application': True,
}