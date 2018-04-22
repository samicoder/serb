from __future__ import unicode_literals
import frappe


def get_context(context):
    context.no_cache = 1
    link = frappe.form_dict['title']
    #web_controller = frappe.get_list("Web Controller", fields=["link", "description", "video_source"], filters={"link": link}, as_list=1)
    web_controller = frappe.db.sql("""select link, description, video_source from `tabWeb Controller`\
                                    where link=%s """, (link.encode('utf8')), as_dict=True)
    if web_controller:
        context.videos = web_controller


