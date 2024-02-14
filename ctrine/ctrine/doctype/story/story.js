// Copyright (c) 2024, Grawish Sachdeva and contributors
// For license information, please see license.txt

frappe.ui.form.on("Story", {
  onload(frm) {
    //        frm.get_field('hours').grid.cannot_add_rows = true;
    //        this.frm.get_field("hours").grid.only_sortable();

    frm.add_custom_button("Add Task", () => {
      doctype = "Task";
      opts = { custom_parent_story: frm.doc.name };
      return new Promise((resolve) => {
        if (opts && $.isPlainObject(opts)) {
          frappe.route_options = opts;
        }
        frappe.model.with_doctype(doctype, function () {
          if (frappe.create_routes[doctype]) {
            frappe
              .set_route(frappe.create_routes[doctype])
              .then(() => resolve());
          } else {
            frappe.ui.form
              .make_quick_entry(
                doctype,
                (doc) => {
                  frm.set_value("hours", [
                    ...frm.doc.hours,
                    {
                      task: doc.name,
                    },
                  ]);
                },
                null
              )
              .then(() => resolve());
          }
        });
      });
    });
  },
  refresh(frm) {
    //  check if form is new
    if (frm.is_new()) {
      frm.add_custom_button("Add Task", () => {
        doctype = "Task";
        opts = { custom_parent_story: frm.doc.name };
        return new Promise((resolve) => {
          if (opts && $.isPlainObject(opts)) {
            frappe.route_options = opts;
          }
          frappe.model.with_doctype(doctype, function () {
            if (frappe.create_routes[doctype]) {
              frappe
                .set_route(frappe.create_routes[doctype])
                .then(() => resolve());
            } else {
              frappe.ui.form
                .make_quick_entry(
                  doctype,
                  (doc) => {
                    frm.set_value("hours", [
                      ...frm.doc.hours,
                      {
                        task: doc.name,
                      },
                    ]);
                  },
                  null
                )
                .then(() => resolve());
            }
          });
        });
      });
    }

    frm.set_query("task", "hours", () => {
      return {
        filters: [
          ["Task", "project", "=", frm.doc.parent_project],
          ["Task", "custom_parent_story", "=", frm.doc.name],
        ],
      };
    });
  },
  add_tasks(frm) {
    doctype = "Task";
    opts = { custom_parent_story: frm.doc.name };
    return new Promise((resolve) => {
      if (opts && $.isPlainObject(opts)) {
        frappe.route_options = opts;
      }
      frappe.model.with_doctype(doctype, function () {
        if (frappe.create_routes[doctype]) {
          frappe.set_route(frappe.create_routes[doctype]).then(() => resolve());
        } else {
          frappe.ui.form
            .make_quick_entry(
              doctype,
              (doc) => {
                frm.set_value("hours", [
                  ...frm.doc.hours,
                  {
                    task: doc.name,
                  },
                ]);
              },
              null
            )
            .then(() => resolve());
        }
      });
    });
  },
});

frappe.ui.form.on("Story", "validate", (frm) => {
  console.log({ frm });
  frm.doc.hours.map((hour) => {
    if (hour.date < frm.doc.start_date || hour.date > frm.doc.end_date) {
      frappe.msgprint(
        __("You can not select before story start or after story ends")
      );
      frappe.validated = false;
    }
  });
});
