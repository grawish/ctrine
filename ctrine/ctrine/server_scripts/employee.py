import frappe
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def make_employee(source_name, target_doc=None):

    doc = get_mapped_doc(
        "Job Applicant",
        source_name,
        {
            "Job Applicant": {
                "doctype": "Employee",
                "field_map": {
                    'applicant_name':'employee_name',
                    'custom_first_name':'first_name',
                    'custom_last_name':'last_name',
                    'custom_present_address':'current_address',
                    'custom_permanent_address':'permanent_address',
                    'custom_pan_number':'pan_number',
                    'custom_aadhar_number':'custom_aadhar_number',
                    'custom_uan':'custom_uan_number',
                    'email_id':'personal_email',
                    'phone_number':'cell_number',  
                },
            },
            "Employee Education": {
				"doctype": "Employee Education",
				"field_map": {
					"school_univ": "school_univ",
					"qualification": "qualification",
					"level": "level",
					"year_of_passing": "year_of_passing",
					"class_per": "class_per",
					"maj_opt_subj": "maj_opt_subj"
				},
        }
        },
        target_doc
    )
    print(doc,"udwhiuegbufgewggfgefggef")
    return doc
