# Copyright 2017 Creu Blanca
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MedicalCareplanAddPlanDefinition(models.TransientModel):
    _inherit = "medical.careplan.add.plan.definition"

    coverage_id = fields.Many2one(
        "medical.coverage", related="careplan_id.coverage_id", readonly=True
    )
    center_id = fields.Many2one(
        "res.partner", related="careplan_id.center_id", readonly=True
    )
    coverage_template_id = fields.Many2one(
        "medical.coverage.template",
        related="coverage_id.coverage_template_id",
        readonly=True,
    )
    agreement_ids = fields.Many2many(
        "medical.coverage.agreement", compute="_compute_agreements"
    )
    agreement_line_id = fields.Many2one("medical.coverage.agreement.item")
    product_id = fields.Many2one(
        "product.product",
        related="agreement_line_id.product_id",
        readonly=True,
    )
    plan_definition_id = fields.Many2one(
        comodel_name="workflow.plan.definition",
        related="agreement_line_id.plan_definition_id",
        readonly=True,
    )
    authorization_method_id = fields.Many2one(
        "medical.authorization.method",
        related="agreement_line_id.authorization_method_id",
        readonly=True,
    )
    authorization_format_id = fields.Many2one(
        "medical.authorization.format",
        related="agreement_line_id.authorization_format_id",
        readonly=True,
    )
    authorization_required = fields.Boolean(
        related="agreement_line_id.authorization_method_id." "authorization_required",
        readonly=True,
    )
    authorization_number = fields.Char()
    authorization_number_extra_1 = fields.Char()
    authorization_information = fields.Text(
        related="agreement_line_id.authorization_format_id."
        "authorization_information",
        readonly=True,
    )
    authorization_extra_1_information = fields.Text(
        related="authorization_format_id.authorization_extra_1_information",
        readonly=True,
    )
    requires_authorization_extra_1 = fields.Boolean(
        related="authorization_format_id.requires_authorization_extra_1",
        readonly=True,
    )
    performer_id = fields.Many2one(
        "res.partner", domain=[("is_practitioner", "=", True)]
    )
    performer_required = fields.Boolean(
        default=False,
        related="agreement_line_id.plan_definition_id.performer_required",
        readonly=True,
    )

    def _get_careplan_date(self):
        return self.careplan_id.encounter_id.create_date or self.careplan_id.create_date

    @api.depends("coverage_template_id", "center_id")
    def _compute_agreements(self):
        for rec in self:
            date = rec._get_careplan_date()
            rec.agreement_ids = self.env["medical.coverage.agreement"].search(
                [
                    (
                        "coverage_template_ids",
                        "=",
                        rec.coverage_template_id.id,
                    ),
                    ("center_ids", "=", rec.center_id.id),
                    ("date_from", "<=", date),
                    "|",
                    ("date_to", "=", False),
                    ("date_to", ">=", date),
                ]
            )

    def _get_values(self):
        values = super(MedicalCareplanAddPlanDefinition, self)._get_values()
        values["coverage_id"] = self.careplan_id.coverage_id.id
        values["coverage_agreement_item_id"] = self.agreement_line_id.id
        values["authorization_method_id"] = self.authorization_method_id.id
        values["authorization_number"] = self.authorization_number
        values["authorization_number_extra_1"] = self.authorization_number_extra_1
        values[
            "coverage_agreement_id"
        ] = self.agreement_line_id.coverage_agreement_id.id
        values["plan_definition_id"] = self.plan_definition_id.id
        values["center_id"] = self.center_id.id
        if self.performer_required:
            values["performer_id"] = self.performer_id.id
        return values

    def _run(self):
        res = super()._run()
        if res and not self.careplan_id.service_id:
            self.careplan_id.write({"service_id": self.product_id.id})
        return res
