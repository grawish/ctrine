frappe.ui.form.on('Task', {
    onload: function(frm) {

        if (frappe.user_roles.includes('Project User')){
            frm.set_df_property('progress', 'read_only', 0);
        }



    }
});