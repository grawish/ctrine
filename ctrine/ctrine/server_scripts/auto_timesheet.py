import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def auto_create_timesheets():
    try:
        # Get all employees
        employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])

        # Calculate the start date of the current week (Monday)
        start_of_week = (datetime.today().date()) - timedelta(days=(datetime.today().date()).weekday())
        # Calculate the end date of the current week (Sunday)
        end_of_week = start_of_week + timedelta(days=6)

        for employee in employees:
            # Check if timesheet already exists for this employee within the current week
            timesheets_exist = frappe.db.exists("Timesheet", {
                "employee": employee["name"],
                "start_date": (">=", start_of_week),
                "end_date": ("<=", end_of_week)
            })

            if not timesheets_exist:
                # Create a new timesheet
                new_timesheet = frappe.get_doc({
                    "doctype": "Timesheet",
                    "employee": employee["name"],
                    "workflow_state": "Draft",  # Set the initial state
                })

                # Append time logs for each day of the week
                for i in range(7):
                    current_day = start_of_week + timedelta(days=i)
                    new_timesheet.append("time_logs", {
                        "from_time": datetime.combine(current_day, datetime.min.time()),
                        # You can set other fields here (e.g., to_time, project, task, etc.)
                    })

                new_timesheet.insert()
                frappe.logger('Ts-NEW').exception(f"Created new timesheet: {new_timesheet.name}")
            else:
                frappe.logger('Ts-exist').exception(f"Timesheet exists for {employee['name']} during {start_of_week} to {end_of_week}")

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

