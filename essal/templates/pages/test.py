from __future__ import unicode_literals
import frappe

def get_context(context):
	return {"data":frappe.get_list("User",fields=["*"])}
