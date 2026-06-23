# Copyright (c) 2026, I-Varse Technologies NG and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe.model.document import Document


class FactoryConfiguration(Document):
    def validate(self):
        if self.is_new() and frappe.db.exists("Factory Configuration", "Factory Configuration"):
            frappe.throw("Only one Factory Configuration record is allowed.")
