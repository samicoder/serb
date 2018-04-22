from frappe import _

def get_data():
	return [
		{
			"label": _("Web Site"),
			"items": [
				{
					"type": "doctype",
					"name": "Web Controller",
					"description": _("Controller for website Details")
				}
			]
		}
	]
