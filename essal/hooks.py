# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "essal"
app_title = "Essal"
app_publisher = "www.essal.io"
app_description = "Essal ERP"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@essal.io"
app_version = "0.0.1"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
		# "/assets/essal/css/bootstrap-rtl.min.css",
		#"assets/essal/css/essal.css"
]

web_include_js = ["assets/js/essal-web.min.js"]
web_include_css = [
	"assets/css/essal-web.css",
	"assets/essal/css/custom.css"
]

#app_include_js = ["assets/js/essal-desk.min.js"]

app_include_css = [
#    "/assets/essal/css/bootstrap-flipped.css",
#    "/assets/essal/css/bootstrap-flipped.css.map",
#    "/assets/essal/css/bootstrap-flipped.min.css",
#    "/assets/essal/css/bootstrap-rtl.css",
#    "/assets/essal/css/bootstrap-rtl.css.map",
#    "/assets/essal/css/bootstrap-rtl.min.css"
]

#website_context = {
#	"favicon": 	"/assets/essal/img/favicon.jpg",
#	"splash_image": "/assets/essal/img/png/essal_logo_150.png"
#}

# include js, css files in header of web template
# web_include_css = "/assets/essal/css/essal.css"
# web_include_js = "/assets/essal/js/essal.js"

# Home Pages
# ----------


# http://fonts.googleapis.com/earlyaccess/amiri.css


# application home page (will override Website Settings)
home_page = "home"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "essal.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "essal.install.before_install"
# after_install = "essal.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "essal.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"essal.tasks.all"
# 	],
# 	"daily": [
# 		"essal.tasks.daily"
# 	],
# 	"hourly": [
# 		"essal.tasks.hourly"
# 	],
# 	"weekly": [
# 		"essal.tasks.weekly"
# 	]
# 	"monthly": [
# 		"essal.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "essal.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "essal.event.get_events"
# }

override_whitelisted_methods = {
    "send_success_email": "essal.templates.pages.main.send_site_details_email"
}
