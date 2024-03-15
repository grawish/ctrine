import frappe

@frappe.whitelist()
def reason(**kwargs):
    try:
        if kwargs.get('docname'):
            frappe.db.set_value('Timesheet', kwargs.get('docname'), {
            'reason': kwargs.get('reason'),
        })

            return "success"
    except Exception as e:
        return None