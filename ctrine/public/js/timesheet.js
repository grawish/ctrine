frappe.ui.form.on('Timesheet', {
    refresh:function(frm){
        
            // Set filters for "project" field in "Timesheet Detail" child table
            frm.fields_dict['time_logs'].grid.get_field('project').get_query = function(doc, cdt, cdn) {
                var child = locals[cdt][cdn];
                return {
                    filters: [
                        ['Project', 'name', 'in', getAssignedProjects()]  // Call function to get assigned projects
                    ]
                };
            };
            console.log(getAssignedProjects())

    },
    setup: function(frm) {
        let user_settings =  {
            "updated_on": "Mon Apr 22 2024 14:57:11 GMT+0530",  // Timestamp indicating when the settings were last updated
            "List": {
                "filters": [],  // List of filters applied to the list view
                "sort_by": "creation",  // Field used for sorting
                "sort_order": "asc"  // Sorting order (ascending or descending)
            },
            "last_view": "List",  // Last view used by the user
            "GridView": {
                "Timesheet Detail": [  // Column configuration for the grid view of "Timesheet Detail" doctype
                    {"fieldname": "from_time", "columns": 1},  // Column configuration for the "from_time" field
                    {"fieldname": "to_time", "columns": 1},    // Column configuration for the "to_time" field
                    {"fieldname": "project", "columns": 1},    // Column configuration for the "project" field
                    {"fieldname": "task", "columns": 1},       // Column configuration for the "task" field
                    {"fieldname": "is_billable", "columns": 1}, // Column configuration for the "is_billable" field
                    {"fieldname": "billing_hours", "columns": 1}, // Column configuration for the "billing_hours" field
                    {"fieldname": "hours", "columns": 1},      // Column configuration for the "hours" field
                    {"fieldname": "custom_tool_used", "columns": 1}, // Column configuration for the "custom_tool_used" field
                    {"fieldname": "activity_type", "columns": 1},   // Column configuration for the "activity_type" field
                    {"fieldname": "description", "columns": 1}      // Column configuration for the "description" field
                ]
            }
        }

        frappe.call({
            method: 'frappe.model.utils.user_settings.save',
            args: {
                doctype:'Timesheet',
                user_settings
            },
            callback: function(response) {
                frm.refresh_fields()
                // // Handle the response from the API call
                // if (response.message && response.message.status === 'success') {
                //     frappe.msgprint('User settings saved successfully.');
                // } else {
                //     frappe.msgprint('Error saving user settings.');
                // }
            }
        });
    }
});

frappe.ui.form.on('Timesheet Detail', {
    task: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var task = child.task;

        if (task) {
            frappe.db.get_doc('Task', task).then(function(doc) {
                if (doc && doc.status === 'Hold') {
                    frappe.model.set_value(cdt, cdn, 'task', '');
                    frappe.msgprint('Hold task not allowed.');
                }
            });
        }
    }
});


function getAssignedProjects() {
    var projects = [];
    // Fetch project names from API
    frappe.call({
        method: 'ctrine.ctrine.server_scripts.timesheet.get_assigned_project_to_user',
        async: false,
        callback: function(response) {
                projects = response.message;
        }
    });
    return projects;
}





frappe.ui.form.on('Timesheet', {
    onload: function(frm) {
        if (frm.doc.status === 'Approved' || frm.doc.status === 'Cancelled') {
            frm.set_read_only(true);
        }
    },
    refresh: function(frm) {
        // If the timesheet is cancelled, show the Amend button
        if (frm.doc.status === 'Cancelled') {
            frm.page.set_primary_action(__('Amend'), function() {
                // Make a call to fetch the previous data
                frappe.call({
                    method: 'ctrine.ctrine.override.timesheet.create_amended_timesheet',
                    args: {
                        timesheet_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            // Redirect to the newly created timesheet
                            frappe.set_route('Form', 'Timesheet', r.message);
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    }
});
