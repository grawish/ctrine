# Copyright (c) 2024, Grawish Sachdeva and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta

from frappe import _
import json

def execute(filters=None):
    project = filters.get("project")
    project_doc = frappe.get_doc("Project", project)
    columns = get_columns(project_doc)
    data = get_data(filters,project_doc)
    day_wise_col = day_wise_columns(str(project_doc.expected_start_date), str(project_doc.expected_end_date))
    columns.extend(day_wise_col)
    return columns, data

def get_data(filters, project_doc):
    data = []
    assignee = project_doc._assign
    assign_users = json.loads(assignee)
    for user in assign_users:
        f_name = get_full_user_name(user)
        role = get_role(user)[0]
        emp = frappe.get_value("Employee", {"user_id": user})
        daywise_billing_hours = get_timesheet_data(filters, emp)
        frappe.logger("ss").exception(daywise_billing_hours)
        emp_dict = {"col2": role, "col3": f_name}
        emp_dict.update(daywise_billing_hours)
        data.append(emp_dict)
    data.append({"col1": " ", "col2": " "})
    data.append({"col1": "Project Management", "col3": "Planned"})
    data.append({"col3": "Actual"})
    # Fetch stories with 'story_name'
    stories = frappe.get_all('Story', filters={'parent_project': project_doc.name}, fields=['name', 'start_date', 'end_date', 'subject'])  
    for story in stories:
        tasks = frappe.get_all('Task Time', filters={'parent': story.get('name')}, fields=['task'], group_by='task')
        for task in tasks:
            task_doc = frappe.get_doc('Task', task.get('task'))
            day_wise_col = day_wise_data(str(task_doc.get('exp_start_date')), str(task_doc.get('exp_end_date')), "<p style='margin:-10px;height:100px; background-color:blue!important;'></p>")
            week_off_days = get_week_off_date(str(project_doc.expected_start_date), str(project_doc.expected_end_date), "<p style='margin:-10px;height:100px; background-color:black!important;'></p>")
            temp = {"col1": story.get('subject'), "col2": task_doc.subject, "col3": "Planned"}  
            temp.update(day_wise_col)
            temp.update(week_off_days)
            data.append(temp)
            max_date, min_date = get_actual_date(project_doc.name, task_doc.name, filters)
            temp2 = {"col3": "Actual"}
            if max_date and min_date:
                actual_day_data = day_wise_data(str(min_date), str(max_date), "<p style='margin:-10px;height:100px; background-color:green!important;'></p>")
                temp2.update(actual_day_data)
                temp2.update(week_off_days)
            data.append(temp2)
    return data


def get_full_user_name(user=None):
    f_name = frappe.get_value("User", user, "full_name")
    return f_name

def get_role(user=None):
    return frappe.get_roles(user)

def get_actual_date(project,task, filters):
    data = frappe.get_all("Timesheet Detail",{"project":project,"task":task},["from_time","to_time","parent"])
    sorted_data = []
    if not filters.get("include_draft_timesheets"):
        for item in data:
            if frappe.get_value("Timesheet",item.get('parent'),"docstatus") == "1":
                sorted_data.append(item)
    else:
        for item in data:
            if frappe.get_value("Timesheet",item.get('parent'),"docstatus") != "2":
                sorted_data.append(item)
    import datetime
    all_dates = [item['from_time'].strftime('%Y-%m-%d') for item in sorted_data] + [item['to_time'].strftime('%Y-%m-%d') for item in sorted_data]
    if all_dates:
        date_objects = [datetime.datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in all_dates]

        max_date = max(date_objects)
        min_date = min(date_objects)
        return max_date, min_date
    return None, None

def get_week_off_date(start_date, end_date, color): 
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    # Generate date range between start and end dates
    date_range = [start_datetime + timedelta(days=x) for x in range((end_datetime - start_datetime).days + 1)]

    # Filter out only Saturday and Sunday dates
    formatted_dates = {}
    for date in date_range:
        if date.weekday() in [5, 6]:  # 5 represents Saturday, 6 represents Sunday
            formatted_dates[date.strftime("%d-%m-%y")] = color

    return formatted_dates

def day_wise_data(start_date, end_date, color):

    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    # Generate date range between start and end dates
    date_range = [start_datetime + timedelta(days=x) for x in range((end_datetime - start_datetime).days + 1)]

    # Convert date objects to strings in the format "dd-mm-yy"
    formatted_dates = {date.strftime("%d-%m-%y"): color for date in date_range}
    return formatted_dates 

def day_wise_columns(start_date,end_date):

    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    # Generate date range between start and end dates
    date_range = [start_datetime + timedelta(days=x) for x in range((end_datetime - start_datetime).days + 1)]

    # Convert date objects to strings in the format "dd-mm-yy"
    formatted_dates = [
    {
        "fieldname": date.strftime("%d-%m-%y"),
        "label": _(date.strftime("%d-%m-%y")),
        "fieldtype": "Data",
        "width": "90"
    } for date in date_range
    ]

    return formatted_dates

def get_columns(project_doc):
    columns = [
        {
            "fieldname":"col1",
            "label": _(""),
            "fieldtype": "Data",
            "width": "180"
        },
        {
            "fieldname":"col2",
            "label": _(""),
            "fieldtype": "Data",
            "width": "180"
        },
        {
            "fieldname":"col3",
            "label": _(""),
            "fieldtype": "Data",
            "width": "180"
        }
        
    ]
    return columns


def get_timesheet_data(filters,emp):
    record_filters = []
    if not filters.get("include_draft_timesheets"):
        record_filters.append(["docstatus", "=", 1])
    else:
        record_filters.append(["docstatus", "!=", 2])
    record_filters.append(["employee", "=", emp])

    timesheets = frappe.get_all(
        "Timesheet", filters=record_filters, fields=["employee", "employee_name", "name"]
    )
    timesheet_ids = [item['name'] for item in timesheets]
    total_billing_hours = get_timesheet_details(filters,timesheet_ids)
    return total_billing_hours


def get_timesheet_details(filters, timesheet):
    timesheet_details_filter = {"parent": ["in", timesheet]}

    timesheet_details_filter["project"] = filters.project
    timesheet_details = frappe.get_all(
        "Timesheet Detail",
        filters=timesheet_details_filter,
        fields=[
            "from_time",
            "to_time",
            "hours",
            "is_billable",
            "billing_hours",
            "billing_rate",
            "parent",
        ],
    )
    daywise_billing_hours = frappe._dict()  # Using Frappe's dictionary
    
    for item in timesheet_details:
        billing_hours = item.get('billing_hours', 0.0)
        date = item.get('from_time').date()  # Extract date from from_time
        day_key = date.strftime('%d-%m-%y')  # Correct date formatting
        
        # Check if key exists, if not initialize it with 0.0
        if day_key not in daywise_billing_hours:
            daywise_billing_hours[day_key] = 0.0
        
        daywise_billing_hours[day_key] += billing_hours
    return daywise_billing_hours