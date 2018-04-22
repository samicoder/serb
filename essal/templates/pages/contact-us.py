# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils import now

def get_context(context):
	doc = frappe.get_doc("Contact Us Settings", "Contact Us Settings")

	if doc.query_options:
		query_options = [opt.strip() for opt in doc.query_options.replace(",", "\n").split("\n") if opt]
	else:
		query_options = ["Sales", "Support", "General"]

	address = None
	if doc.get("address"):
		address = frappe.get_doc("Address", doc.address)

	out = {
		"query_options": query_options
	}
	out.update(doc.as_dict())

	return out

max_communications_per_hour = 1000

@frappe.whitelist(allow_guest=True)
def send_message(subject="Website Query", message="", sender="",client_name=None,topic_type="general_inquires",company_name=None):

    client_name =client_name
    topic_type = topic_type

    company_name= company_name
    if not message:
    	frappe.response["message"] = 'من فضلك اكتب نص الرسالة'
    	return
    if not sender:
    	frappe.response["message"] = 'من فضلك ادخل الايميل'
    	return
    # guest method, cap max writes per hour
    if frappe.db.sql("""select count(*) from `tabCommunication`
		where `sent_or_received`="Received"
		and TIMEDIFF(%s, modified) < '01:00:00'""", now())[0][0] > max_communications_per_hour:
		frappe.response["message"] = "Sorry: we believe we have received an unreasonably high number of requests of this kind. Please try later"
		return

    # send email
    forward_to_email = frappe.db.get_value("Contact Us Settings", None, "forward_to_email")
    message_details = "نوع الاستفسار: "

    if topic_type == "general_inquires":
        message_details= message_details+" استفسارات عامة "
    else:
        message_details = message_details+" شكوى "+" \n"

    if company_name is not None:
        message_details= message_details+" اسم الشركة:  "
        message_details= message_details+company_name +" \n "

    if client_name is not None:
        message_details = message_details+ "اسم العميل: " +client_name+" \n"

    message_details= message_details+"الرسالة: "
    message = message+message_details

    if forward_to_email:
    	frappe.sendmail(recipients=forward_to_email, sender=sender, content=message, subject=subject)
    return "okay"
