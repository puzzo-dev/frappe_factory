"""Sync agent interface called by the `opsedge-sync` service.

Endpoints:
    GET  /api/method/frappe_factory.sync.api.get_pending_records
    POST /api/method/frappe_factory.sync.api.mark_synced
    POST /api/method/frappe_factory.sync.api.log_sync_result

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
    """Return pending local records for the opsedge-sync agent to push to cloud."""
    _validate_api_key()
    limit = frappe.utils.cint(frappe.request.args.get("limit", 100))
    since = frappe.request.args.get("since")
    filters = [["status", "!=", "Success"]]
    if since:
        filters.append(["modified", ">", since])

    records = frappe.get_all(
        "OpsEdge Sync Log",
        filters=filters,
        fields=["name", "sync_direction", "sync_started_at", "status", "records_attempted", "records_synced", "records_failed"],
        limit=limit,
        order_by="modified asc",
    )
    return {"records": records}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def mark_synced():
    """Mark a sync log as successfully synced."""
    _validate_api_key()
    data = frappe.request.get_json() or {}
    name = data.get("name")
    if not name:
        frappe.throw("name is required", frappe.MandatoryError)
    frappe.db.set_value("OpsEdge Sync Log", name, "status", "Success")
    frappe.db.commit()
    return {"status": "ok", "name": name}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def log_sync_result():
    """Create a sync log entry from the opsedge-sync agent."""
    _validate_api_key()
    data = frappe.request.get_json() or {}
    doc = frappe.get_doc({
        "doctype": "OpsEdge Sync Log",
        "sync_direction": data.get("sync_direction", "Local→Cloud"),
        "sync_started_at": data.get("sync_started_at") or frappe.utils.now(),
        "sync_completed_at": data.get("sync_completed_at") or frappe.utils.now(),
        "status": data.get("status", "Success"),
        "records_attempted": data.get("records_attempted", 0),
        "records_synced": data.get("records_synced", 0),
        "records_failed": data.get("records_failed", 0),
        "conflict_count": data.get("conflict_count", 0),
        "triggered_by": data.get("triggered_by", "Scheduler"),
        "error_log": frappe.as_json(data.get("errors", [])),
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "ok", "name": doc.name}


def cleanup_old_sync_logs():
    """Daily scheduled task: delete OpsEdge Sync Log rows older than 90 days."""
    cutoff = frappe.utils.add_days(frappe.utils.today(), -90)
    frappe.db.sql(
        "DELETE FROM `tabOpsEdge Sync Log` WHERE modified < %s",
        cutoff,
    )
    frappe.db.commit()
