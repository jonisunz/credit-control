# Copyright 2016-2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_unpaid_margin = fields.Integer(
        config_param="account_financial_risk.invoice_unpaid_margin", readonly=False
    )

    def set_values(self):
        params = self.env["ir.config_parameter"].sudo()
        before_margin = int(
            params.get_param("account_financial_risk.invoice_unpaid_margin")
        )
        super().set_values()
        after_margin = self.invoice_unpaid_margin
        if before_margin != after_margin:
            self.env.cr.execute(
                "SELECT DISTINCT partner_id FROM account_move_line "
                "WHERE partner_id IS NOT NULL"
            )
            partners = (
                self.env["res.partner"]
                .sudo()
                .browse([r[0] for r in self.env.cr.fetchall()])
            )
            partners._compute_risk_account_amount()
