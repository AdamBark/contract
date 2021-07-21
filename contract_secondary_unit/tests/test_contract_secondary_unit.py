# Copyright 2021 Akretion - Kevin Roche
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestContractSecondaryUnit(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.product_uom_gram = cls.env.ref("uom.product_uom_gram")
        cls.product_uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product = cls.env["product.product"].create(
            {
                "name": "test",
                "uom_id": cls.product_uom_kg.id,
                "uom_po_id": cls.product_uom_kg.id,
                "secondary_uom_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "unit-700",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.5,
                        },
                    )
                ],
            }
        )
        cls.secondary_unit = cls.env["product.secondary.unit"].search(
            [("product_tmpl_id", "=", cls.product.product_tmpl_id.id)]
        )
        cls.product.contract_secondary_uom_id = cls.secondary_unit.id
        cls.partner = cls.env["res.partner"].create({"name": "test - partner"})

        cls.contract = cls.env["contract.contract"].create(
            {
                "name": "Test Contract",
                "partner_id": cls.partner.id,
                "contract_type": "sale",
                "contract_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "name": cls.product.name,
                            "quantity": 2,
                            "uom_id": cls.product.uom_id.id,
                            "price_unit": 100,
                            "recurring_rule_type": "monthly",
                            "recurring_interval": 1,
                            "date_start": "2021-06-01",
                            "recurring_next_date": "2021-07-01",
                        },
                    )
                ],
            }
        )

    def test_onchange_secondary_uom(self):
        self.contract.contract_line_ids.write(
            {"secondary_uom_id": self.secondary_unit.id, "secondary_uom_qty": 5}
        )
        self.contract.contract_line_ids._compute_quantity()
        self.assertEqual(self.contract.contract_line_ids.quantity, 2.5)

    def test_onchange_secondary_unit_quantity(self):
        self.contract.contract_line_ids.update(
            {"secondary_uom_id": self.secondary_unit.id, "quantity": 4}
        )
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_qty, 8.0)

    def test_onchange_order_product_uom(self):
        self.contract.contract_line_ids.update(
            {
                "secondary_uom_id": self.secondary_unit.id,
                "uom_id": self.product_uom_gram.id,
                "quantity": 3500.00,
            }
        )
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_qty, 7.0)

    def test_independent_type(self):
        # dependent type is already tested as dependency_type by default
        self.contract.contract_line_ids.secondary_uom_id = self.secondary_unit.id
        self.contract.contract_line_ids.secondary_uom_id.write(
            {"dependency_type": "independent"}
        )

        self.contract.contract_line_ids.write({"secondary_uom_qty": 10})
        self.assertEqual(self.contract.contract_line_ids.quantity, 2)
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_qty, 10)

        self.contract.contract_line_ids.write({"quantity": 17})
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_qty, 10)
        self.assertEqual(self.contract.contract_line_ids.quantity, 17)

    def test_secondary_uom_unit_price(self):
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_unit_price, 0)
        self.contract.contract_line_ids.update(
            {"secondary_uom_id": self.secondary_unit.id, "quantity": 2}
        )

        self.assertEqual(self.contract.contract_line_ids.secondary_uom_qty, 4)
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_unit_price, 50)

        self.contract.contract_line_ids.write({"quantity": 4})
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_qty, 8)
        self.assertEqual(self.contract.contract_line_ids.secondary_uom_unit_price, 50)
        self.assertEqual(self.contract.contract_line_ids.price_subtotal, 400)
