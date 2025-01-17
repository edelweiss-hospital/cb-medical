# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MedicalTurn(models.Model):
    _name = "medical.turn"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date asc"
    _description = "Medical Turn"

    center_ids = fields.Many2many(
        string="Centers",
        required=True,
        comodel_name="res.partner",
        domain=[("is_center", "=", True)],
        tracking=True,
    )
    practitioner_id = fields.Many2one(
        string="Practitioner",
        comodel_name="res.partner",
        tracking=True,
    )
    specialty_id = fields.Many2one(
        "medical.turn.specialty", tracking=True, required=True
    )
    turn_tag_ids = fields.Many2many(
        comodel_name="medical.turn.tag", related="specialty_id.turn_tag_ids"
    )
    date = fields.Datetime(
        required=True,
        copy=False,
        index=True,
        tracking=True,
        default=lambda r: fields.Datetime.now(),
    )
    duration = fields.Float("Duration (in hours)", tracking=True, required=True)

    @api.depends("practitioner_id", "center_ids", "specialty_id")
    def _compute_display_name(self):
        return super()._compute_display_name()

    def name_get(self):
        result = []
        for rec in self:
            name = "{} [{}] ({})".format(
                rec.specialty_id.name,
                rec.practitioner_id.display_name or _("Pending to assign"),
                ",".join([c.ref or c.name for c in rec.center_ids]),
            )
            result.append((rec.id, name))
        return result
