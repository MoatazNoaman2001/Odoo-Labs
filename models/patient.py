from odoo import models, fields, api
from datetime import datetime


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    email = fields.Char(string='Email', required=True, unique=True)
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR Test')
    age = fields.Integer()
    image = fields.Image()

    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        domain=[('is_opened', '=', True)],
        required=True
    )

    department_capacity = fields.Integer(
        string='Department Capacity',
        compute='_compute_department_capacity',
        store=True
    )
    doctor_ids = fields.Many2many('hms.doctors', string="Doctors")

    # State
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    # Logs
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Logs")

    @api.depends('department_id')
    def _compute_department_capacity(self):
        for rec in self:
            rec.department_capacity = rec.department_id.capacity if rec.department_id else 0

    @api.onchange('state')
    def _onchange_state(self):
        if self.state:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description': f"State changed to {self.state}",
                'created_by': self.env.user.id,
                'date': fields.Datetime.now()
            })

    @api.onchange('age')
    def _onchange_age_set_pcr(self):
        if self.age and self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Checked",
                    'message': "PCR has been automatically checked because age is below 30."
                }
            }
