
import frappe
from datetime import timedelta


@frappe.whitelist()
def submit_overdue_timesheets(): 
    overdue_timesheets = frappe.get_all("Timesheet", filters={"status": "Draft"}, fields=["name", "start_date"])
    
    for timesheet in overdue_timesheets:
        try:
            project_hours = {}
            is_hours_valid = True
            # Get Timesheet document
            time_doc = frappe.get_doc("Timesheet", timesheet.get('name'))
            # Access child table entries
            timesheet_details = time_doc.get("time_logs")
            # Calculate total hours for each project
            for log in timesheet_details:
                if log.project_name in project_hours:
                    project_hours[log.project_name] += log.hours
                else:
                    project_hours[log.project_name] = log.hours
            frappe.logger('ProjectHours').exception(project_hours)
            # Check if any project exceeds 24 hours
            for project, hours in project_hours.items():
                if hours > 24:
                    is_hours_valid = False
                    break
            
            # Submit the timesheet if it's overdue and the hours are valid
            if is_hours_valid:
                start_date = timesheet.start_date
                days_to_sunday = (3 - start_date.weekday()) % 7  # Calculate days until Sunday
                next_sunday = start_date + timedelta(days=days_to_sunday)
                #frappe.logger('dayCheck').exception(f'ST:{start_date},End:{next_sunday}')
                if next_sunday == frappe.utils.now_datetime().date():  # Check if Sunday is the current day 
                    frappe.db.set_value("Timesheet", timesheet.name, "docstatus", 1)
                    frappe.db.set_value("Timesheet", timesheet.name, "workflow_state", "Submitted")
                    frappe.db.set_value("Timesheet", timesheet.name, "status", "Submitted")
                    frappe.db.commit()                    
        except Exception as e:
            frappe.log_error(f"Error submitting timesheet {timesheet.name}: {e}")

