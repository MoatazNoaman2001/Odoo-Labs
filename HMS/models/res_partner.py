from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    related_patient_id = fields.Many2one("hms.patient", string="Related Patient")
    
    @api.constrains('related_patient_id', 'email')
    def _check_patient_email_unique(self):
        for partner in self:
            if partner.related_patient_id and partner.related_patient_id.email:
                other_partners = self.search([
                    ('id', '!=', partner.id),
                    ('related_patient_id', '!=', partner.related_patient_id.id),
                    ('email', '=', partner.related_patient_id.email)
                ])
                if other_partners:
                    raise ValidationError(_("This patient's email is already linked to another customer."))
