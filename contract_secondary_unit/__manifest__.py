# Copyright 2021 Akretion - Kevin Roche
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Contract Secondary Unit",
    "summary": "Contract line in a secondary unit",
    "version": "14.0.1.0.0",
    "category": "Contract",
    "website": "https://github.com/OCA/contract",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": ["contract", "product_secondary_unit"],
    "data": [
        "views/abstract_contract_line.xml",
    ],
}
