"""Sync agent interface called by the `opsedge-sync` service.

Endpoints:
    GET  /api/method/frappe_factory.sync.api.get_pending_records
    POST /api/method/frappe_factory.sync.api.mark_synced
    POST /api/method/frappe_factory.sync.api.log_sync_result

All endpoints require API key authentication. The key is read from
Factory Configuration (opsedge_sync_api_key) first, falling back to
frappe.conf.opsedge_sync_api_key for backward compatibility.
"""

from __future__ import annotations

import logging

import frappe
from frappe.utils import add_days, cint, today

logger = logging.getLogger(__name__)

SYNC_API_LIMIT = 500
SYNC_API_WINDOW = 60


def _get_api_key():
    """Prefer database-stored API key; fallback to frappe.conf."""
    settings = frappe.get_single("Factory Configuration")
    key = settings.get_password("opsedge_sync_api_key") or frappe.get_conf().get("opsedge_sync_api_key")
    return key


def _check_rate_limit(key, max_requests=SYNC_API_LIMIT, window=SYNC_API_WINDOW):
    """Best-effort Redis-based rate limiting."""
    try:
        cache = frappe.cache()
        cache_key = f"frappe_factory:rate_limit:{key}"
        current = cint(cache.get(cache_key) or 0) + 1
        if current == 1:
            cache.set_value(cache_key, current, expires_in_sec=window)
        else:
            cache.set_value(cache_key, current)
        if current > max_requests:
            frappe.throw("Rate limit exceeded", frappe.RateLimitExceededError)
    except frappe.RateLimitExceededError:
        raise
    except Exception:
        logger.exception("Rate limiter unavailable; allowing request")


def _validate_api_key():
    key = frappe.request.headers.get("X-OpsEdge-API-Key") if frappe.request else None
    expected = _get_api_key()
    if not expected or key != expected:
        frappe.throw("Invalid API key", frappe.AuthenticationError)
    _check_rate_limit("sync_api_key")


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_pending_records():
    """Return pending local records for the opsedge-sync agent to push to cloud."""
    _validate_api_key()
    limit = cint(frappe.request.args.get("limit", 100))
    if limit < 1 or limit > 1000:
        frappe.throw("limit must be between 1 and 1000", frappe.ValidationError)

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

    if not frappe.db.exists("OpsEdge Sync Log", name):
        frappe.throw(f"Sync log {name} not found", frappe.DoesNotExistError)

    frappe.db.set_value("OpsEdge Sync Log", name, "status", "Success")
    frappe.db.commit()
    return {"status": "ok", "name": name}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def log_sync_result():
    """Create a sync log entry from the opsedge-sync agent."""
    _validate_api_key()
    data = frappe.request.get_json() or {}

    direction = data.get("sync_direction", "Local→Cloud")
    if direction not in ("Local→Cloud", "Cloud→Local"):
        frappe.throw("Invalid sync_direction", frappe.ValidationError)

    status = data.get("status", "Success")
    if status not in ("Running", "Success", "Partial", "Failed"):
        frappe.throw("Invalid status", frappe.ValidationError)

    triggered_by = data.get("triggered_by", "Scheduler")
    if triggered_by not in ("Scheduler", "Manual", "Forced"):
        frappe.throw("Invalid triggered_by", frappe.ValidationError)

    doc = frappe.get_doc({
        "doctype": "OpsEdge Sync Log",
        "sync_direction": direction,
        "sync_started_at": data.get("sync_started_at") or frappe.utils.now(),
        "sync_completed_at": data.get("sync_completed_at") or frappe.utils.now(),
        "status": status,
        "records_attempted": cint(data.get("records_attempted", 0)),
        "records_synced": cint(data.get("records_synced", 0)),
        "records_failed": cint(data.get("records_failed", 0)),
        "conflict_count": cint(data.get("conflict_count", 0)),
        "triggered_by": triggered_by,
        "error_log": frappe.as_json(data.get("errors", [])),
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "ok", "name": doc.name}


def cleanup_old_sync_logs():
    """Daily scheduled task: delete OpsEdge Sync Log rows older than 90 days."""
    cutoff = add_days(today(), -90)
    try:
        rows = frappe.db.sql(
            "DELETE FROM `tabOpsEdge Sync Log` WHERE modified < %s",
            cutoff,
        )
        frappe.db.commit()
        logger.info("Deleted %s old sync log rows before %s", rows, cutoff)
    except Exception:
        logger.exception("Failed to clean up old sync logs")
        raise
