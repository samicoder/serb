# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = True


def get_context(context):
    # context.no_cache = 1

    # context.email = 'eyad@gmail.com'  # frappe.form_dict['email']
    form_data = dict()

    # form_data['full_name'] = 'Eyad Farra'
    # form_data['mobile_number'] = '0597333268'
    # form_data['association_name'] = 'test association_name'
    # form_data['email'] = 'eyad.farra@exa.com.sa'

    context['form_data'] = form_data
    return context


@frappe.whitelist(allow_guest=True)
def join_us(association_name, email, name, mobile_number, state=None, city=None, activity=None, employee_count=None):
    # Check for duplication
    if frappe.db.exists(
            "Join Us",
            {
                "email": email
            }
    ):
        frappe.response["message"] = _('This email is already used!', "ar"),
        return

    frappe.get_doc(dict(
        doctype='Join Us',
        association_name=association_name,
        email=email,
        full_name=name,
        mobile_number=mobile_number,
        state=state,
        city=city,
        activity=activity,
        employee_count=employee_count,
    )).insert(ignore_permissions=True)

    return "okay", _("You will Receive an email with full details soon", "ar")
