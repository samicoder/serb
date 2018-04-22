
frappe.ready(function() {

	$('.btn-lg').off("click").on("click", function() {

		var email = $('[name="emai"]').val();
		var password = $('[name="password"]').val();

		if(!(email)) {
			msgprint(__("Please enter your email"));
			$('[name="email"]').focus();
			return false;
		} 
		else if(!(password)) {
			msgprint(__("Please enter your password"));
			$('[name="password"]').focus();
			return false;
		}

		else if(!valid_email(email)) {
			msgprint(__("Please enter a valid email address"));
			$('[name="email"]').focus();
			return false;
		}
                else {

		$("#contact-alert").toggle(false);
		frappe.call({
			type: "POST",
			method: "essal.templates.pages.main.signup_new_user",
			btn: this,
			args: {
				email: email,
				company_name: password
			},
			callback: function(r) {
				if(r.message[0]==="okay") {
					msgprint(r.message[1], "success");
				} else {
					msgprint(__(r.message[0]));
					console.log(r.exc);
				}
				$(':input').val('');
                                return false;
			}
		});
                }
	return false;
	});


});

var msgprint = function(txt, type) {
	type = type || "warning";
	console.warn(txt);
	if(txt) {
		var contact_alert = $("#contact-alert");
		contact_alert.removeClass("alert-warning alert-success");
		contact_alert.addClass("alert-" + type).html(txt).toggle(true);
    }
};
