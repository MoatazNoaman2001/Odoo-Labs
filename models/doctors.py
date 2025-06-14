from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctors'
    _description = 'Doctors'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Image()
    patient_ids = fields.Many2many('hms.patient', string="Patients")
