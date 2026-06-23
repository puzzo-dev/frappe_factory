# Copyright (c) 2026, I-Varse  Technologies NG and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe.model.document import Document


class PlantFloorLayout(Document):
	def validate(self):
		if self.is_active:
			existing = frappe.db.get_value(
				"Plant Floor Layout",
				{"zone_type": self.zone_type, "is_active": 1, "name": ("!=", self.name)},
				"name",
			)
			if existing:
				frappe.throw(
					f"Layout {existing} is already active for zone type {self.zone_type}. Deactivate it first."
				)
			self.last_published = frappe.utils.now()

	def before_save(self):
		for widget in self.widgets:
			if widget.iot_device and not widget.thingsboard_device_id:
				widget.thingsboard_device_id = frappe.db.get_value(
					"IoT Device Registry", widget.iot_device, "thingsboard_device_id"
				)
