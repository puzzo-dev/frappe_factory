# Copyright (c) 2026, I-Varse Technologies NG and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe.model.document import Document


class MachineTelemetryLog(Document):
    def validate(self):
        if not self.iot_device:
            frappe.throw("IoT Device is required")
        if self.metric_value is None:
            frappe.throw("Metric value is required")
        if not self.recorded_at:
            frappe.throw("Recorded at timestamp is required")
