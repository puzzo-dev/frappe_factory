"""ThingsBoard REST API client for Frappe IOT.

All ThingsBoard calls go through this module. Never call the TB API directly
from a DocType controller.
"""

from __future__ import annotations

import frappe


class ThingsBoardClient:
    def __init__(self, base_url: str | None = None, tenant_token: str | None = None):
        settings = frappe.get_single("Factory Configuration")
        self.base_url = (base_url or settings.thingsboard_url or "http://localhost:8080").rstrip("/")
        self.tenant_token = tenant_token or settings.get_password("thingsboard_tenant_token")

    def get_device_credentials(self, device_id: str) -> dict:
        """Return device credentials for a given ThingsBoard device ID."""
        pass

    def get_telemetry(self, device_id: str, keys: list[str] | None = None, start_ts: int | None = None, end_ts: int | None = None) -> dict:
        """Fetch latest or historical telemetry for a device."""
        pass

    def send_attributes(self, device_id: str, attributes: dict) -> dict:
        """Push server-side attributes to a ThingsBoard device."""
        pass
