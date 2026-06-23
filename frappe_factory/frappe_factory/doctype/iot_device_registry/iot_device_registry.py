# Copyright (c) 2026, I-Varse Technologies NG and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe.model.document import Document


class IoTDeviceRegistry(Document):
    def validate(self):
        if self.thingsboard_device_id:
            existing = frappe.db.get_value(
                "IoT Device Registry",
                {"thingsboard_device_id": self.thingsboard_device_id},
                "name",
            )
            if existing and existing != self.name:
                frappe.throw(f"ThingsBoard device ID {self.thingsboard_device_id} is already linked to {existing}.")
