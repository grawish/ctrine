
import frappe
from datetime import timedelta


@frappe.whitelist()
def submit_overdue_timesheets(): 
    overdue_timesheets = frappe.get_all("Timesheet", filters={"workflow_state": "draft"}, fields=["name", "start_date"])
    try:
        if overdue_timesheets:
            for timesheet in overdue_timesheets:
                # Get Timesheet document
                time_doc = frappe.get_doc("Timesheet", timesheet.get('name'))
                # Access child table entries
                timesheet_details = time_doc.get("time_logs")
                start_date = timesheet.start_date
                if start_date and time_doc.get('employee_name') and time_doc.workflow_state=="draft":
                    days_to_sunday = (5 - start_date.weekday()) % 7 
                    next_sunday = start_date + timedelta(days=days_to_sunday)
                    if next_sunday == frappe.utils.now_datetime().date():  # Check if Sunday is the current day 
                        frappe.db.set_value("Timesheet", timesheet.name, "docstatus", 0)
                        frappe.db.set_value("Timesheet", timesheet.name, "workflow_state", "Submitted")
                        frappe.db.set_value("Timesheet", timesheet.name, "status", "Draft")
                        frappe.db.commit()                    
    except Exception as e:
        frappe.log_error(f"Error submitting timesheet {timesheet.name}: {e}")

