
import frappe
from datetime import timedelta


@frappe.whitelist()
def submit_overdue_timesheets(): 
    overdue_timesheets = frappe.get_all("Timesheet", filters={"status": "Draft"}, fields=["name", "start_date"])
    
    for timesheet in overdue_timesheets:
        try:
            # Get Timesheet document
            time_doc = frappe.get_doc("Timesheet", timesheet.get('name'))
            # Access child table entries
            timesheet_details = time_doc.get("time_logs")
            start_date = timesheet.start_date
            if start_date:
                days_to_sunday = (6 - start_date.weekday()) % 7  # Calculate days until Sunday
                next_sunday = start_date + timedelta(days=days_to_sunday)
                #frappe.logger('dayCheck').exception(f'ST:{start_date},End:{next_sunday}')
                if next_sunday == frappe.utils.now_datetime().date():  # Check if Sunday is the current day 
                    frappe.db.set_value("Timesheet", timesheet.name, "docstatus", 1)
                    frappe.db.set_value("Timesheet", timesheet.name, "workflow_state", "Submitted")
                    frappe.db.set_value("Timesheet", timesheet.name, "status", "Submitted")
                    frappe.db.commit()                    
        except Exception as e:
            frappe.log_error(f"Error submitting timesheet {timesheet.name}: {e}")

