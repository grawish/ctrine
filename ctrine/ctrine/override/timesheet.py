from erpnext.projects.doctype.timesheet.timesheet import Timesheet
import frappe
from frappe.utils import flt
from frappe import _


class CustomTimesheet(Timesheet):
    # def before_save(self):
    #     print('hssh')
    # def on_update(self):
    #     print(frappe.as_json(self),"--")
        
    def on_submit(self):
        self.validate_mandatory_fields()
        self.update_task_and_project()

    def validate_mandatory_fields(self):
        for data in self.time_logs:
            if not data.from_time and not data.to_time:
                frappe.throw(_("Row {0}: From Time and To Time is mandatory.").format(data.idx))

            if not data.activity_type and self.employee:
                frappe.throw(_("Row {0}: Activity Type is mandatory.").format(data.idx))

            # if flt(data.hours) == 0.0:
            #     frappe.throw(_("Row {0}: Hours value must be greater than zero1.").format(data.idx))

    def update_task_and_project(self):
        tasks, projects = [], []

        for data in self.time_logs:
            if data.task and data.task not in tasks:
                task = frappe.get_doc("Task", data.task)
                task.update_time_and_costing()
                task.save()
                tasks.append(data.task)

            elif data.project and data.project not in projects:
                frappe.get_doc("Project", data.project).update_project()
                projects.append(data.project)

 
def on_update(doc,method):
    if len(doc.time_logs)>0:
        task_wise_actual_hours_map = {}
        for tlog in doc.time_logs:
            if tlog.get('task') and tlog.get('hours'):
                task_wise_actual_hours_map[tlog.get('task')] = task_wise_actual_hours_map.get(tlog.get('task'),0) + float(tlog.get('hours'))
        
        if len(task_wise_actual_hours_map):
            for task,hours in task_wise_actual_hours_map.items():
                task_doc = frappe.get_doc("Task",task)
                task_doc.actual_hours = hours
                task_doc.save()
            frappe.db.commit()   
            
        

@frappe.whitelist()
def create_amended_timesheet(timesheet_name):
    # Fetch the previous timesheet data
    prev_timesheet = frappe.get_doc("Timesheet", timesheet_name)

    # Create a new timesheet with the previous data
    new_timesheet = frappe.copy_doc(prev_timesheet)
    new_timesheet.status = "Draft"  # Optionally change the status to Draft
    new_timesheet.workflow_state = "Draft"
    # new_timesheet.amended_from = timesheet_name  # Keep track of the original timesheet
    new_timesheet.insert()

    return new_timesheet.name

        