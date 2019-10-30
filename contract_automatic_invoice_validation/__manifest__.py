# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Contract Automatic Invoice Validation',
    'summary': 'Allow automatic validation of reccuring invoices',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Akretion,'
              'Odoo Community Association (OCA)',
    'website': 'http://github.com/oca/contract',
    'depends': ['contract'],
    'category': 'Accounting',
    'data': [
        'views/contract_view.xml',
    ],
    'installable': True,
}
