import frappe
@frappe.whitelist()
def fetch_hours(project_name):
    total_hours=0
    #frappe.throw(project_name)
    stories=frappe.get_all('Story',filters={'parent_project':project_name})
    frappe.logger('stories').exception(stories)
    for story in stories:
        frappe.logger('story').exception(story)
        story_doc=frappe.get_doc('Story',story.get('name'))
        child_doc=story_doc.get('hours')
        #frappe.logger('child_doc').exception(child_doc)
        for row in child_doc:
            frappe.logger('CHILDHOURS').exception(row.hours)
            total_hours += int(row.hours)
    frappe.logger('TotalHours').exception(total_hours)

    # Return the total hours
    return total_hours