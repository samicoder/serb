/**
 * Created by aquaider on 9/28/16.
 */
// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

frappe.ready(function () {

    $('.join-us-send').off("click").on("click", function () {
        var name = $('[name="name"]').val();
        var mobile_number = $('[name="mobile_number"]').val();
        var association_name = $('[name="association_name"]').val();
        var email = $('[name="email"]').val();
        var state = $('[name="state"]').val();
        var city = $('[name="city"]').val();
        var activity = $('[name="activity"]').val();
        var employee_count = $('[name="employee_count"]').val();

        if (!name) {
            $('[name="name"]').focus();
            msgprint(__("من فضلك ادخل اسمك"));
            return false;
        } else if (!mobile_number) {
            $('[name="mobile_number"]').focus();
            msgprint(__("من فضلك ادخل رقم جوالك"));
            return false;
        } else if (!association_name) {
            $('[name="mobile_number"]').focus();
            msgprint(__("من فضلك ادخل اسم الجمعية"));
            return false;
        } else if (!email) {
            $('[name="email"]').focus();
            msgprint(__("من فضلك ادخل البريد الالكتروني"));
            return false;
        } else if (!valid_email(email)) {
            msgprint(__("من فضلك ادخل بريد الكتروني صحيح"));
            $('[name="email"]').focus();
            return false;
        }

        var params = {
            association_name: association_name,
            email: email,
            name: name,
            mobile_number: mobile_number,
            state: state,
            city: city,
            activity: activity,
            employee_count: employee_count
        };
        for(var i in params){
            if(!params[i]){
                delete params[i];
            }
        }

        $("#contact-alert").toggle(false);
        frappe.call({
            type: "POST",
            method: "essal.templates.pages.join-us.join_us",
            btn: this,
            args: params,
            callback: function (r) {
                if (r.message[0] === "okay") {
                    msgprint(r.message[1], "success");
                } else {
                    msgprint(__(r.message[0]));
                    console.log(r.exc);
                }
                $(':input').val('');
                return false;
            }
        });
        return false;
    });

});

var msgprint = function (txt) {
    if (txt) $(".join-us-alert").html(txt).toggle(true);
};
