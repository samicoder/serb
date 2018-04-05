frappe.provide('erpnext');

// add toolbar icon
$(document).bind('toolbar_setup', function() {
    console.log("toolbat setup")
    frappe.app.name = "Essal";

    frappe.help_feedback_link = '<p><a class="text-muted" \
        href="https://4.essal.io">Feedback</a></p>'


    $('.navbar-home').html('<img class="erpnext-icon" src="'+
            frappe.urllib.get_base_url()+'/assets/essal/img/favicon.jpg" />');


});