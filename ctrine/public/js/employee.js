// frappe.ui.form.on('Employee', {
//     refresh(frm) {
//         if (frm.doc.job_applicant) {
//             frappe.call({
//                 method: 'frappe.client.get',
//                 args: {
//                     doctype: 'Job Applicant',
//                     name: frm.doc.job_applicant
//                 },
            
//                  callback: function(r) {
//                      var applicant = r.message;
//                      console.log("Applicant data: ", applicant);

//                      // Fill in the details from the Job Applicant
//                      frm.set_value('first_name', applicant.custom_first_name);
//                      frm.set_value('last_name', applicant.custom_last_name);
//                      frm.set_value('date_of_birth', applicant.date_of_birth);
//                     //  frm.set_value('gender', applicant.gender);
//                     //  frm.set_value('company', applicant.company_name);
//                      frm.set_value('designation', applicant.designation);
//                      frm.set_value('custom_uan_number', applicant.custom_uan);
//                      frm.set_value('custom_aadhar_number', applicant.custom_aadhar_number);
//                      frm.set_value('pan_number', applicant.custom_pan_number);
//                      frm.set_value('personal_email', applicant.email_id);
//                      frm.set_value('cell_number', applicant.phone_number);
//                      frm.set_value('current_address', applicant.custom_present_address);
//                      frm.set_value('permanent_address', applicant.custom_permanent_address);
//                      frm.set_value('educational_qualification', applicant.custom_education);
                    
//                      frm.refresh_fields();

//                     //  console.log("Form refreshed");
//                     // frm.save();



                     
  
             
//                 }
//             });
            
//         }
//     }
// });

frappe.ui.form.on('Employee', {
    before_save(frm) {
        if (frm.doc.job_applicant) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Job Applicant',
                    name: frm.doc.job_applicant
                },
                callback: function(r) {
                    if (r.message) {
                        var applicant = r.message;
                        console.log("Applicant data: ", applicant);

                        // Fill in the details from the Job Applicant
                        frm.set_value('first_name', applicant.custom_first_name);
                        frm.set_value('last_name', applicant.custom_last_name);
                        frm.set_value('date_of_birth', applicant.date_of_birth);
                        // frm.set_value('gender', applicant.gender);
                        // frm.set_value('company', applicant.company_name);
                        frm.set_value('designation', applicant.designation);
                        frm.set_value('custom_uan_number', applicant.custom_uan);
                        frm.set_value('custom_aadhar_number', applicant.custom_aadhar_number);
                        frm.set_value('pan_number', applicant.custom_pan_number);
                        frm.set_value('personal_email', applicant.email_id);
                        frm.set_value('cell_number', applicant.phone_number);
                        frm.set_value('current_address', applicant.custom_present_address);
                        frm.set_value('permanent_address', applicant.custom_permanent_address);
                        frm.set_value('educational_qualification', applicant.custom_education);

                        frm.refresh_fields();
                    } 
                }
            });
        }
    }
});



