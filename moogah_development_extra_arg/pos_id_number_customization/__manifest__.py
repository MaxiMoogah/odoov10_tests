# -*- coding: utf-8 -*-
{
    'name': "POS Identification Number Customization",
    'summary': """POS Identification Number Customization""",
    'description': """
    This module allows the search of customers by Main Identification Number.
    """,
    'author': "Moogah",
    'website': "www.moogah.com",
    'category': 'Point of Sale',
    'version': '10.0.1.0',
    'depends': ['l10n_ar_partner', 'point_of_sale'],
    'qweb': [
    ],
    'data': [
        'views/pos_id_number_customization_view.xml',
    ],
    'demo': [],
    'installable': True,
}
