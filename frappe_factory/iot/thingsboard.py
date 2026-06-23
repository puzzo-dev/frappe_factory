"""ThingsBoard REST API client for Frappe Factory.

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

    @property
    def headers(self) -> dict:
        return {"Content-Type": "application/json", "X-Authorization": f"Bearer {self.tenant_token or ''}"}

    @classmethod
    def get_client(cls) -> "ThingsBoardClient":
        return cls()

    def get_device_credentials(self, device_id: str) -> dict:
        """Return device credentials for a given ThingsBoard device ID."""
        import requests
        url = f"{self.base_url}/api/device/{device_id}/credentials"
        response = requests.get(url, headers=self.headers, timeout=5)
        response.raise_for_status()
        return response.json()

    def get_telemetry(self, device_id: str, keys: list[str] | None = None, start_ts: int | None = None, end_ts: int | None = None) -> dict:
        """Fetch latest telemetry for a device."""
        import requests
        params = {}
        if keys:
            params["keys"] = ",".join(keys)
        if start_ts:
            params["startTs"] = start_ts
        if end_ts:
            params["endTs"] = end_ts
        url = f"{self.base_url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def send_attributes(self, device_id: str, attributes: dict) -> dict:
        """Push server-side attributes to a ThingsBoard device."""
        import requests
        url = f"{self.base_url}/api/plugins/telemetry/DEVICE/{device_id}/attributes/SERVER_SCOPE"
        response = requests.post(url, json=attributes, headers=self.headers, timeout=5)
        response.raise_for_status()
        return response.json() if response.text else {}
