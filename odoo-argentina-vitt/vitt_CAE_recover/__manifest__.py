# -*- coding: utf-8 -*-
{
    'name': "Recuperacion de Cod. CAE desde Factura",
    'summary': """Recuperar CAE desde la factura y/o lista de facturas""",
    'description': """
        Recuperar CAE desde la factura
    """,
    'author': "Moogah",
    'website': "http://www.Moogah.com",
    'category': 'Uncategorized',
    'version': '10.0.1.0.6',
    'depends': [
        'account',
        'l10n_ar_afipws_fe',
        'l10n_ar_account',
    ],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'application': True,
}