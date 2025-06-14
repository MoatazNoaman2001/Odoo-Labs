from odoo import models, fields, api

class HMSPatientLog(models.Model):
    _name = "hms.patient.log"
    _description = "Patient Log History"
    _order = "create_date desc"
    
    patient_id = fields.Many2one("hms.patient", string="Patient", required=True, ondelete="cascade")
    created_by = fields.Many2one("res.users", string="Created By", default=lambda self: self.env.user, readonly=True)
    date = fields.Datetime(string="Date", default=fields.Datetime.now, readonly=True)
    description = fields.Text(string="Description", required=True)
