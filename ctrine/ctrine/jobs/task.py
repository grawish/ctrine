import frappe

@frappe.whitelist()
def put_child_task_on_hold():
    tasks = frappe.get_all('Task',filters={'status':'Overdue','is_group':1},fields=['name'])
    child_task_list =  []
    for task in tasks:
        child_tasks  = frappe.get_all('Task',filters ={'status':('!=','Cancelled'),'parent_task':task.get('name')},fields=['name'])
        if len(child_tasks):
            child_task_list.extend([ i.get('name') for i in child_tasks])
    if len(child_task_list):        
        query = """ Update `tabTask` t set t.status = 'Hold' WHERE t.name IN %(li)s """
        frappe.db.sql(query,{'li':tuple(child_task_list)})  
        frappe.db.commit()
        return query


def on_update(doc,method):
    old_doc = doc.get_doc_before_save()  
    if old_doc and doc.get('status') == 'Overdue':
        put_child_task_on_hold()
             