{
    'name': 'HMS - Hospital Management System',
    "summary": "Comprehensive hospital management for patients, records, and staff",
     "description": """
        HMS module to efficiently manage:
        - Patients
        - Medical Records
        - Medical History
        - Departments
        - Doctors
    """,
    'author': 'Moataz Noaman',
    'version': '1.0',
    'depends': ['base','crm'],
    'data': [
        "security/ir.model.access.csv",
        'views/patient_view.xml',
        'views/menu.xml',
        'views/department_view.xml',
        'views/doctors_view.xml',
        "views/patient_log_view.xml",
        'views/res_partner_view.xml',
    ],
    "application": True,
    "installable": True,
}
