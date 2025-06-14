from odoo import models, fields, api

class HMSDoctors(models.Model):
    _name = "hms.doctors"
    _description = "Hospital Doctors"
    _rec_name = "full_name"
    
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Binary(string="Image")
    patient_ids = fields.Many2many("hms.patient", "doctor_patient_rel", "doctor_id", "patient_id", string="Patients")
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)
    
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for doctor in self:
            doctor.full_name = f"{doctor.first_name} {doctor.last_name}" if doctor.first_name and doctor.last_name else ""
