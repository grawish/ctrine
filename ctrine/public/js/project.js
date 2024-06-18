frappe.ui.form.on('Project', {
    refresh: function(frm) {
        // Add a custom button to the form
        frm.add_custom_button(__('Project Time Plan Report'), function() {
            // Your logic for the button click
            frappe.route_options = {
                "project": frm.doc.name
            };
            frappe.set_route("query-report", "Project Report");
        }, __("View"));
    }
});
