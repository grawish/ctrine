
from datetime import datetime
import frappe
@frappe.whitelist()
def fetch_hours(project_name,from_date):
    total_hours=0
    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    stories=frappe.get_all('Story',filters={'parent_project':project_name})
    if stories and from_date:
        for story in stories:
            story_doc=frappe.get_doc('Story',story.get('name'))
            child_doc=story_doc.get('hours')
            for row in child_doc:
                frappe.logger('row_date').exception(f"{type(row.date)},{type(from_date)},{row.date == from_date}")
                if(row.date and row.date == from_date):
                    total_hours += int(row.hours)
        return total_hours