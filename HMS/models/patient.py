from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError
import re

class HMSPatient(models.Model):
    _name = "hms.patient"
    _description = "Hospital Patient"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    birth_date = fields.Date(string="Birth Date", required=True)
    history = fields.Html(string="History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection([
        ("a", "A"),
        ("b", "B"),
        ("ab", "AB"),
        ("o", "O"),
    ], string="Blood Type")
    pcr = fields.Boolean(string="PCR")
    image = fields.Binary(string="Patient Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    email = fields.Char(string="Email", required=True, index=True)

    department_id = fields.Many2one("hms.department", string="Department", domain="[('is_opened', '=', True)]")
    doctor_ids = fields.Many2many("hms.doctors", "doctor_patient_rel", "patient_id", "doctor_id", string="Doctors")
    created_by = fields.Many2one("res.users", string="Created By", default=lambda self: self.env.user)
    description = fields.Text(string="Description")
    state = fields.Selection([
        ("undetermined", "Undetermined"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("serious", "Serious"),
    ], string="State", default="undetermined")
    log_ids = fields.One2many("hms.patient.log", "patient_id", string="Log History")

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email must be unique!'),
    ]

    @api.depends("birth_date")
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0

    @api.onchange("pcr")
    def _onchange_pcr(self):
        if not self.pcr:
            self.cr_ratio = 0.0

    @api.constrains("pcr", "cr_ratio")
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError(_("CR Ratio is required when PCR is checked."))

    @api.onchange("department_id")
    def _onchange_department_id(self):
        if not self.department_id:
            self.doctor_ids = [(5, 0, 0)]  # Clear the many2many field

    department_capacity = fields.Integer(related="department_id.capacity", string="Department Capacity", readonly=True)

    @api.onchange("age")
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': _("Patient Age Alert"),
                    'message': _("PCR has been automatically checked as the patient is younger than 30 years old.")
                }
            }
    
    def write(self, vals):
        if 'state' in vals and vals['state'] != self.state:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description': f"State changed to {dict(self._fields['state'].selection).get(vals['state'])}"
            })
        return super(HMSPatient, self).write(vals)
        
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError(_("Please enter a valid email address"))
