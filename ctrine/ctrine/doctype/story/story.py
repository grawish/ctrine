import frappe
from frappe.utils import now
from frappe.model.document import Document
from frappe.utils.user import get_user_fullname
from frappe.desk.form.assign_to import add as add_assign_to

class Story(Document):
    def on_update(self):
        if self.hours:
            task_details = get_task_specific_data(self.hours)
            for task, task_info in task_details.items():
                # Update Task document using SQL query
                frappe.db.sql("""
                    UPDATE `tabTask`
                    SET exp_end_date = %s,
                        exp_start_date = %s,
                        expected_time = %s
                    WHERE name = %s
                """, (task_info.get('end_date'), task_info.get('start_date'), task_info.get('hours'), task))
                
                # Assign the task to users
                add_assign_to(args={
                    'assign_to': task_info.get('user_ids', []),
                    'doctype': 'Task',
                    'name': task,
                    'description': f"Task '{task}' assigned to {self.name} story",
                    'priority': 'Medium',  # Adjust priority as needed
                    'date': task_info.get('end_date'),
                    'assigned_by': frappe.session.user,
                    're_assign': False
                },ignore_permissions= True)



def assign_task_to_user(task, user_id):
    # Check if a ToDo record already exists for the task and user
    if frappe.db.exists('ToDo', {'reference_type': 'Task', 'reference_name': task, 'owner': user_id}):
        return  # ToDo record already exists, so no need to create a new one
    
    # Create a ToDo record for the assignment
    todo = frappe.get_doc({
        'doctype': 'ToDo',
        'owner': user_id,
        'description': f"Task '{task}' assigned to {get_user_fullname(user_id)}",
        'reference_type': 'Task',
        'reference_name': task,
        'date': now(),
        'priority': 'Medium',  # Adjust priority as needed
        'status': 'Open'
    })
    todo.insert(ignore_permissions=True)  # Ignore permissions to allow assignment by any user



def get_task_specific_data(data):
    task_data = {}
    for i in data:
        task = i.task
        if task not in task_data:
            task_data[task] = {
                'date': [],
                'person': [],
                'hours': 0,
                'start_date': None,
                'end_date': None,
                'user_ids': []  # List to store user_ids
            }
        task_data[task]['date'].append(i.date)
        task_data[task]['person'].append(i.person)
        task_data[task]['hours'] += float(i.hours)
    
    # Calculate start_date and end_date for each task
    for task, task_info in task_data.items():
        dates = task_info['date']
        if dates:
            task_info['start_date'] = min(dates)
            task_info['end_date'] = max(dates)
        
        # Fetch user_id for each person (employee ID)
        employees = frappe.get_all('Employee', filters={'name': ('in', task_info['person'])}, fields=['user_id'])
        task_info['user_ids'] = [emp['user_id'] for emp in employees]

    return task_data
