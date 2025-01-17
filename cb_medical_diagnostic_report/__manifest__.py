# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Medical Diagnostic Report",
    "summary": """Allows the creation of medical diagnostic reports""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca",
    "website": "https://github.com/tegin/cb-medical",
    "depends": [
        "medical_diagnostic_report",
        "medical_base",
        "medical_signature_storage",
        "sequence_parser",
        "medical_encounter_identifier",
        "web_drop_target",
        "web_tree_image_tooltip",
        "storage_file",
    ],
    "data": [
        "data/ir_parameter.xml",
        "security/department_security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/medical_department.xml",
        "views/medical_diagnostic_report_template.xml",
        "views/medical_diagnostic_report.xml",
        "views/medical_report_category.xml",
        "reports/medical_diagnostic_report_template.xml",
        "wizards/medical_diagnostic_report_expand.xml",
        "templates/assets.xml",
    ],
    "demo": ["demo/medical_diagnostic_report.xml"],
}
