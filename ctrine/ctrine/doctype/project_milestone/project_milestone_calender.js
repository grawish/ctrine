// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Project Milestone"] = {
	field_map: {
		"start": "expected_start_date",
		"end": "expected_end_date",
		"id": "name",
		"title": "subject_line",
		"allDay": "allDay",
		"progress": "progress"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "parent_project",
			"options": "Project",
			"label": __("Project")
		}
	],
	get_events_method: "frappe.desk.calendar.get_events"
}
