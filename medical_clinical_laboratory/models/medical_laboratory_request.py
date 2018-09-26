# Copyright 2017 Creu Blanca
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MedicalLaboratoryRequest(models.Model):
    # FHIR Entity: Procedure request
    # (https://www.hl7.org/fhir/procedurerequest.html)
    _name = 'medical.laboratory.request'
    _description = 'Laboratory Request'
    _inherit = 'medical.request'

    internal_identifier = fields.Char(
        string="Laboratory request"
    )
    laboratory_event_ids = fields.One2many(
        string='Related Procedure',
        comodel_name='medical.laboratory.event',
        inverse_name='laboratory_request_id',
        readonly=True,
    )
    laboratory_event_count = fields.Integer(
        compute="_compute_laboratory_event_count",
        string='# of Events',
        copy=False,
    )

    @api.depends('laboratory_event_ids')
    def _compute_laboratory_event_count(self):
        for rec in self:
            rec.laboratory_event_count = len(rec.laboratory_event_ids.ids)

    def _get_internal_identifier(self, vals):
        return self.env['ir.sequence'].next_by_code(
            'medical.laboratory.request') or '/'

    def _get_parent_field_name(self):
        return 'laboratory_request_id'

    def action_view_request_parameters(self):
        return {
            'view':
                'medical_clinical_laboratory.'
                'medical_laboratory_request_action',
            'view_form': 'medical.procedure.request.view.form', }

    @api.multi
    def action_view_laboratory_events(self):
        self.ensure_one()
        action = self.env.ref(
            'medical_clinical_laboratory.medical_laboratory_event_action')
        result = action.read()[0]

        result['context'] = {
            'default_patient_id': self.patient_id.id,
            'default_performer_id': self.performer_id.id,
            'default_laboratory_request_id': self.id,
            'default_name': self.name,
        }
        result['domain'] = "[('laboratory_request_id', '=', " + \
                           str(self.id) + ")]"
        if len(self.procedure_ids) == 1:
            res = self.env.ref('medical.laboratory.event.view.form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.procedure_ids.id
        return result