# Copyright (c) 2026, I-Varse Technologies NG and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe.model.document import Document


class ProductionFloorEvent(Document):
	def on_submit(self):
		if self.resolved_at and self.event_time:
			self.duration_minutes = round(
				(frappe.utils.get_datetime(self.resolved_at) - frappe.utils.get_datetime(self.event_time)).total_seconds() / 60,
				2,
			)
