{
    "name": "Hospital Management System",
    "summary": "Manage hospital patients and records",
    "description": """
        Hospital Management System module for managing:
        - Patients
        - Patient Records
        - Medical History
        - Departments
        - Doctors
    """,
    "author": "mohamed abdel AaL",
    "category": "Health",
    "version": "1.0",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/hms_menus.xml",
        "views/patient_views.xml",
        "views/department_views.xml",
        "views/doctors_views.xml",
        "views/patient_log_views.xml",
        "views/res_partner_views.xml",
    ],
    "application": True,
    "installable": True,
}
