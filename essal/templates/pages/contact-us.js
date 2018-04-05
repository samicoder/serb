/**
 * Created by aquaider on 9/28/16.
 */
// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function() {

	$('.cu-btn-send').off("click").on("click", function() {
		var email = $('[name="email"]').val();
		var message = $('[name="message"]').val();
		var client_name = $('[name="client_name"]').val();
		var company_name = $('[name="company_name"]').val();
		var topic_type = $('[name="topic_type"]').val();
		var topic_title = $('[name="topic_title"]').val();

		if(!(email && message)) {
			msgprint(__("من فضلك ادخل البريد الالكتروني ونص الرسالة"));
			return false;
		}

		if(!valid_email(email)) {
				msgprint(__("من فضلك ادخل البريد الالكتروني"));
				$('[name="email"]').focus();
				return false;
		}

		$("#contact-alert").toggle(false);
		frappe.send_message({
			subject: $('[name="subject"]').val(),
			sender: email,
			message: message,
            client_name:client_name,
            topic_type:topic_type,
            topic_title:topic_title,
            company_name:company_name,
			callback: function(r) {
				if(r.message==="okay") {
					msgprint(__("شكرا لتواصلك معنا"));
				} else {
					msgprint(__("There were errors"));
					console.log(r.exc);
				}
				$(':input').val('');
			}
		}, this);
	return false;
	});

});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}
