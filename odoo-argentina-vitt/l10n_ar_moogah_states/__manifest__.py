# -*- coding: utf-8 -*-
{
    'name': 'Provincias Argentinas con Cod. AFIP',
    'version': '10.0.1.2',
    'category': 'Setup',
    'author': 'Moogah',
    'license': 'AGPL-3',
    'summary': 'App de actualizacion para cod. AFIP en Provincias',
    'description': 'App que actualiza el campo para el codigo AFIP en las provincias de Argentina',
    'depends': ['base'],
    'data': [
        'data/res.country.state.csv',
    ],
    'installable': True,
    'application': False,
}