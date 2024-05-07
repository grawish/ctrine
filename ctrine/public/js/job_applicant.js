frappe.ui.form.on("Job Applicant", {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.status == "Accepted") {
        frm.add_custom_button(
            __("Employee"),
            function () {
                make_employee(frm);
            },
            __("Create"),
        );
    }
}
});

function make_employee(frm) {
    frappe.model.open_mapped_doc({
        method: "ctrine.ctrine.server_scripts.employee.make_employee", // Specify your custom method here
        frm: frm,
    });
}
