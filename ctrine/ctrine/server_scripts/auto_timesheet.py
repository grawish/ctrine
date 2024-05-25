import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def auto_create_timesheets():
    try:
        # Get submitted timesheets
        submitted_timesheets = frappe.get_all("Timesheet", filters={"workflow_state": "Submitted"}, fields=["*"])
        # Calculate the start date of the current week (Monday)
        start_of_week = (datetime.today().date()) - timedelta(days=(datetime.today().date()).weekday())
        # Calculate the end date of the current week (Sunday)
        end_of_week = start_of_week + timedelta(days=6)
        for timesheet in submitted_timesheets:
            time_doc = frappe.get_doc("Timesheet", timesheet['name'])
            if time_doc.get('employee_name'):
                timesheets_exist = frappe.db.exists("Timesheet", {
                        "employee": time_doc.get('employee'),
                        "start_date": (">=", start_of_week),
                        "end_date": ("<=", end_of_week)
                    })
                if not timesheets_exist:
                    new_timesheet = frappe.get_doc({
                        "doctype": "Timesheet",
                        "employee": timesheet["employee"],
                        "workflow_state": "draft",
                    })
                    for i in range(7):
                        current_day = start_of_week + timedelta(days=i)
                        new_timesheet.append("time_logs", {
                            "from_time": datetime.combine(current_day, datetime.min.time()),
                        })
                    new_timesheet.insert()
                    #log the created timesheet for reference
                    frappe.logger('Ts-NEW').exception(f"Created new timesheet: {new_timesheet.name}")
                    
                else:
                    frappe.logger('Ts-exist').exception(f"TS:{timesheet},Timesheet exists for {time_doc.get('employee_name')},Date:{time_doc.get('start_date')}")
    except Exception as e:
        frappe.logger('error_message').exception(f"An error occurred: {str(e)}")


# @frappe.whitelist()
# def auto_submit_timesheets():
#     try:
#         # Get all open timesheets
#         draft_timesheets = frappe.get_all("Timesheet", filters={"workflow_state": "Draft"}, fields=["*"])
        
#         for timesheet in draft_timesheets:
#             time_doc = frappe.get_doc("Timesheet", timesheet.get['name'])
#             # Submit the timesheet
#             time_doc.submit()
#             # Commit the transaction to the database
#             frappe.db.commit()
#             # Log the submitted timesheet for reference
#             frappe.logger('Ts-SUBMIT').exception(f"Submitted timesheet: {time_doc.name}")
            
#     except Exception as e:
#         frappe.logger('error_message').exception(f"An error occurred: {str(e)}")

