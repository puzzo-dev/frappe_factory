"""Webhook receivers for ThingsBoard and ERPNext document events.

ThingsBoard HTTP Integration posts to:
    https://<site>/api/method/frappe_iot.iot.webhooks.<method_name>

Auth: validate the X-OpsEdge-Token header against frappe.conf.opsedge_webhook_token.
"""

from __future__ import annotations

import frappe


def _validate_webhook_token():
    token = frappe.request.headers.get("X-OpsEdge-Token") if frappe.request else None
    expected = frappe.get_conf().get("opsedge_webhook_token")
    if not expected or token != expected:
        frappe.throw("Invalid webhook token", frappe.PermissionError)


@frappe.whitelist(allow_guest=True, methods=["POST"])
def telemetry():
    """Receive telemetry payload from ThingsBoard."""
    _validate_webhook_token()
    pass


@frappe.whitelist(allow_guest=True, methods=["POST"])
def alarm():
    """Receive alarm payload from ThingsBoard."""
    _validate_webhook_token()
    pass


@frappe.whitelist(allow_guest=True, methods=["POST"])
def device_connected():
    """Receive device connected/disconnected event."""
    _validate_webhook_token()
    pass


def on_attendance_submit(doc, method):
    """ERPNext Attendance on_submit hook."""
    pass


def on_quality_submit(doc, method):
    """ERPNext Quality Inspection on_submit hook."""
    pass


def on_work_order_update(doc, method):
    """ERPNext Work Order on_update hook."""
    pass


def check_production_lag():
    """Scheduled hourly check for production lag against n8n threshold."""
    pass
