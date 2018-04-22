# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
from frappe.model.document import Document


class WebController(Document):
    def get_context(context):

        if context.description is None:
            context.description = ''

