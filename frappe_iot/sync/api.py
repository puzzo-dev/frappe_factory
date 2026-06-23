"""Sync agent interface called by the `opsedge-sync` service.

Endpoints:
    GET  /api/method/frappe_iot.sync.api.get_pending_records
    POST /api/method/frappe_iot.sync.api.mark_synced
    POST /api/method/frappe_iot.sync.api.log_sync_result

All endpoints require API key authentication (configured in frappe.conf).
"""

from __future__ import annotations

import frappe


def _validate_api_key():
    key = frappe.request.headers.get("X-OpsEdge-API-Key") if frappe.request else None
    expected = frappe.get_conf().get("opsedge_sync_api_key")
    if not expected or key != expected:
        frappe.throw("Invalid API key", frappe.AuthenticationError)


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_pending_records():
    _validate_api_key()
    pass


@frappe.whitelist(allow_guest=True, methods=["POST"])
def mark_synced():
    _validate_api_key()
    pass


@frappe.whitelist(allow_guest=True, methods=["POST"])
def log_sync_result():
    _validate_api_key()
    pass


def cleanup_old_sync_logs():
    """Daily scheduled task: delete OpsEdge Sync Log rows older than 90 days."""
    cutoff = frappe.utils.add_days(frappe.utils.today(), -90)
    frappe.db.sql(
        "DELETE FROM `tabOpsEdge Sync Log` WHERE modified < %s",
        cutoff,
    )
    frappe.db.commit()
