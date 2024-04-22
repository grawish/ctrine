import frappe

@frappe.whitelist()
def reason(**kwargs):
    try:
        if kwargs.get('docname'):
            frappe.db.set_value('Timesheet', kwargs.get('docname'), {
            'custom_reason': kwargs.get('reason'),
        })

            return "success"
    except Exception as e:
        return None
@frappe.whitelist()
def clrReason(**kwargs):
    try:
        if kwargs.get('docname'):
            frappe.db.set_value("Timesheet",kwargs.get('docname'),{
                'custom_reason':''
            })
        return 'Reason Cleared'
    except Exception as ex:
        frappe.logger('TimeSheet_EX').exception(ex)
        return None