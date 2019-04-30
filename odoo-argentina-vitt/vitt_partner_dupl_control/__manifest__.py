# -*- coding: utf-8 -*-
{
    'name': 'Seteo para control de partner con mismo cuit duplicados',
    'summary': 'Seteo para control de partner con mismo cuit duplicados',
    'description': """Seteo para control de partner con mismo cuit duplicados""",
    'version': '10.0.1.0.4',
    'author': 'Moogah',
    'website': 'http://www.moogah.com',
    'depends': [
        'l10n_ar_account_withholding',
        'vitt_nl_setting',
        'account',
    ],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
}
