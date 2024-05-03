// Copyright (c) 2024, Grawish Sachdeva and contributors
// For license information, please see license.txt

frappe.query_reports["Project Report"] = {
	"filters": [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
			reqd: 1
			
		},
		{
			fieldname: "include_draft_timesheets",
			label: __("Include Timesheets in Draft Status"),
			fieldtype: "Check",
		},
	]
};
