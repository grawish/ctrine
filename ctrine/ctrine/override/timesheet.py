from erpnext.projects.doctype.timesheet.timesheet import Timesheet
import frappe


class CustomTimesheet(Timesheet):
    def before_save(self):
        print('hssh')
    def on_update(self):
        print(frappe.as_json(self),"--")
        

 
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
            
        
        