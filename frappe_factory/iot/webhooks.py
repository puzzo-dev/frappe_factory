"""Webhook receivers for ThingsBoard and ERPNext document events.

ThingsBoard HTTP Integration posts to:
    https://<site>/api/method/frappe_factory.iot.webhooks.<method_name>

Auth: validate the X-OpsEdge-Token header against the token stored in
Factory Configuration (opsedge_webhook_token), falling back to
frappe.conf.opsedge_webhook_token for backward compatibility.
"""

from __future__ import annotations

import logging

import frappe
from frappe.utils import add_days, cint, flt, format_datetime, get_datetime, now, today

logger = logging.getLogger(__name__)


WEBHOOK_TOKEN_LIMIT = 1000
WEBHOOK_TOKEN_WINDOW = 60


def _log_audit(action, affected_doctype=None, affected_docname=None, details=None, source="Webhook", endpoint=None):
    """Write an audit log for a webhook or scheduler-driven change."""
    try:
        ip = None
        user = frappe.session.user if frappe.session else "Guest"
        if frappe.request:
            ip = frappe.request.headers.get("X-Forwarded-For", frappe.request.remote_addr)
            if ip:
                ip = ip.split(",")[0].strip()
        frappe.get_doc({
            "doctype": "OpsEdge Audit Log",
            "timestamp": now(),
            "source": source,
            "endpoint": endpoint,
            "ip_address": ip,
            "user": user,
            "affected_doctype": affected_doctype,
            "affected_docname": affected_docname,
            "action": action,
            "details": frappe.as_json(details) if details else None,
        }).insert(ignore_permissions=True)
    except Exception:
        logger.exception("Failed to write audit log")


def _get_request():
    """Return the current request object (wrapper for testability)."""
    return frappe.request


def _get_request_json():
    """Return JSON body of the current request."""
    req = _get_request()
    return req.get_json() if req else {}


def _get_request_header(name, default=None):
    """Return a header from the current request."""
    req = _get_request()
    return req.headers.get(name, default) if req else default


def _db_get_value(*args, **kwargs):
    """Wrapper for frappe.db.get_value to ease mocking."""
    return frappe.db.get_value(*args, **kwargs)


def _db_set_value(*args, **kwargs):
    """Wrapper for frappe.db.set_value to ease mocking."""
    return frappe.db.set_value(*args, **kwargs)


def _db_exists(*args, **kwargs):
    """Wrapper for frappe.db.exists to ease mocking."""
    return frappe.db.exists(*args, **kwargs)


def _db_sql(*args, **kwargs):
    """Wrapper for frappe.db.sql to ease mocking."""
    return frappe.db.sql(*args, **kwargs)


def _get_config():
    """Return Factory Configuration singleton (cached)."""
    return frappe.get_single("Factory Configuration")


def _get_webhook_token():
    """Prefer database-stored token; fallback to frappe.conf."""
    settings = _get_config()
    token = settings.get_password("opsedge_webhook_token") or frappe.get_conf().get("opsedge_webhook_token")
    return token


def _check_rate_limit(key, max_requests=WEBHOOK_TOKEN_LIMIT, window=WEBHOOK_TOKEN_WINDOW):
    """Best-effort rate limiting via Redis cache.

    Falls back to allowing the request if Redis is unavailable so that
    telemetry ingestion is not silently blocked by cache misconfiguration.
    """
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


def _validate_webhook_token():
    token = _get_request_header("X-OpsEdge-Token")
    expected = _get_webhook_token()
    if not expected or token != expected:
        frappe.throw("Invalid webhook token", frappe.PermissionError)
    _check_rate_limit("webhook_token")


def _lookup_device(tb_device_id):
    """Return active IoT Device Registry record for a ThingsBoard device ID."""
    if not tb_device_id:
        frappe.throw("device_id is required", frappe.MandatoryError)

    device = _db_get_value(
        "IoT Device Registry",
        {"thingsboard_device_id": tb_device_id},
        ["name", "linked_workstation", "is_active"],
        as_dict=True,
    )
    if not device:
        frappe.throw(f"Unknown device {tb_device_id}", frappe.DoesNotExistError)
    return device


def _parse_timestamp(ts):
    """Parse a ThingsBoard millisecond timestamp into a Frappe datetime string."""
    if ts is None:
        return now()
    try:
        return format_datetime(get_datetime(float(ts) / 1000))
    except (ValueError, TypeError, OverflowError) as e:
        logger.warning("Invalid telemetry timestamp %r: %s", ts, e)
        frappe.throw("Invalid timestamp", frappe.ValidationError)


def _parse_metric_value(metric_value):
    """Parse a telemetry metric value to float; log and coerce on failure."""
    if metric_value is None:
        return 0.0
    if isinstance(metric_value, bool):
        return 1.0 if metric_value else 0.0
    try:
        return flt(metric_value)
    except (ValueError, TypeError):
        logger.warning("Could not parse metric value %r as float; defaulting to 0.0", metric_value)
        return 0.0


@frappe.whitelist(allow_guest=True, methods=["POST"])
def telemetry():
    """Receive telemetry payload from ThingsBoard.

    Payload should contain at minimum:
        device_id: ThingsBoard device ID
        ts: Unix timestamp (ms)
        values: dict of metric key -> value
    """
    _validate_webhook_token()
    data = _get_request_json() or {}
    tb_device_id = data.get("device_id")
    device = _lookup_device(tb_device_id)

    if not device.is_active:
        return {"status": "skipped", "reason": "device_inactive"}

    values = data.get("values", {})
    if not isinstance(values, dict):
        frappe.throw("values must be an object", frappe.ValidationError)

    recorded_at = _parse_timestamp(data.get("ts"))
    settings = _get_config()

    if settings.enable_async_telemetry:
        frappe.enqueue(
            "frappe_factory.iot.webhooks._process_telemetry",
            queue="default",
            job_name=f"Process telemetry for {tb_device_id}",
            device=device,
            tb_device_id=tb_device_id,
            values=values,
            recorded_at=recorded_at,
            raw_payload=data,
        )
        return {"status": "queued", "records": len(values)}

    _process_telemetry(device, tb_device_id, values, recorded_at, data)
    frappe.db.commit()
    return {"status": "ok", "records": len(values)}


def _process_telemetry(device, tb_device_id, values, recorded_at, raw_payload):
    """Insert telemetry rows and update workstation status.

    Designed to run synchronously inside the HTTP request or as a background job.
    """
    for metric_key, metric_value in values.items():
        _insert_telemetry(device, tb_device_id, metric_key, metric_value, recorded_at, raw_payload)

    if device.linked_workstation:
        _update_workstation_status(device.linked_workstation, values)
        _log_audit(
            "update_workstation_status",
            affected_doctype="Workstation",
            affected_docname=device.linked_workstation,
            details={"machine_state": values.get("machine_state")},
            endpoint="telemetry",
        )

    _log_audit(
        "ingest_telemetry",
        affected_doctype="Machine Telemetry Log",
        affected_docname=device.name,
        details={"records": len(values), "tb_device_id": tb_device_id},
        endpoint="telemetry",
    )


def _insert_telemetry(device, tb_device_id, metric_key, metric_value, recorded_at, raw_payload):
    metric_float = _parse_metric_value(metric_value)

    frappe.get_doc({
        "doctype": "Machine Telemetry Log",
        "iot_device": device.name,
        "thingsboard_device_id": tb_device_id,
        "recorded_at": recorded_at,
        "metric_key": metric_key,
        "metric_value": metric_float,
        "raw_payload": frappe.as_json(raw_payload),
    }).insert(ignore_permissions=True)


def _update_workstation_status(workstation_name, values):
    """Map telemetry values to Workstation status."""
    state = values.get("machine_state", "Idle")
    status_map = {
        "Running": "Production",
        "Idle": "Idle",
        "Warning": "Problem",
        "Fault": "Problem",
    }
    status = status_map.get(state, "Idle")
    if workstation_name:
        _db_set_value("Workstation", workstation_name, "status", status)


@frappe.whitelist(allow_guest=True, methods=["POST"])
def alarm():
    """Receive alarm payload from ThingsBoard."""
    _validate_webhook_token()
    data = _get_request_json() or {}
    tb_device_id = data.get("device_id")
    device = _lookup_device(tb_device_id)

    event_type = data.get("event_type", "Machine Fault")
    if event_type not in ("Line Stoppage", "Machine Fault", "Quality Hold", "Shift Change", "Maintenance Start", "Maintenance End", "Custom"):
        frappe.throw("Invalid event_type", frappe.ValidationError)

    severity = data.get("severity", "Critical")
    if severity not in ("Info", "Warning", "Critical"):
        frappe.throw("Invalid severity", frappe.ValidationError)

    frappe.get_doc({
        "doctype": "Production Floor Event",
        "event_type": event_type,
        "severity": severity,
        "event_time": now(),
        "iot_device": device.name,
        "linked_workstation": device.linked_workstation,
        "thingsboard_alarm_id": data.get("alarm_id"),
        "description": data.get("details", ""),
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "ok"}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def device_connected():
    """Receive device connected/disconnected event."""
    _validate_webhook_token()
    data = _get_request_json() or {}
    tb_device_id = data.get("device_id")
    connected = data.get("connected", True)
    device = _lookup_device(tb_device_id)

    _db_set_value("IoT Device Registry", device.name, "last_seen", now())
    frappe.db.commit()
    return {"status": "ok", "device": device.name, "connected": connected}


@frappe.whitelist(allow_guest=True, methods=["GET"])
def health_check():
    """Return basic health status for monitoring/load balancers."""
    _validate_webhook_token()
    return {"status": "ok"}


def on_attendance_submit(doc, method):
    """Update Shift Attendance Summary when Attendance is submitted."""
    if not doc.employee or not doc.attendance_date:
        return
    try:
        summary_name = _db_get_value("Shift Attendance Summary", {"shift_date": doc.attendance_date}, "name")
        if not summary_name:
            logger.info("No Shift Attendance Summary found for %s", doc.attendance_date)
            return

        summary = frappe.get_doc("Shift Attendance Summary", summary_name)
        if doc.status == "Present":
            summary.total_present = cint(summary.total_present) + 1
        elif doc.status == "Absent":
            summary.total_absent = cint(summary.total_absent) + 1
        summary.save(ignore_permissions=True)
    except frappe.DoesNotExistError:
        logger.info("Shift Attendance Summary not found for %s", doc.attendance_date)
    except Exception:
        logger.exception("Failed to update attendance summary for %s", doc.name)


def on_quality_submit(doc, method):
    """Create Production Floor Event if Quality Inspection fails."""
    if doc.status != "Rejected":
        return
    try:
        workstation = doc.workstation
        if not workstation and doc.reference_name:
            # Reference may be a Work Order; fetch its workstation from the operation if possible.
            workstation = _db_get_value("Work Order", doc.reference_name, "workstation")

        frappe.get_doc({
            "doctype": "Production Floor Event",
            "event_type": "Quality Hold",
            "severity": "Critical",
            "event_time": now(),
            "linked_workstation": workstation,
            "work_order": doc.reference_name,
            "description": f"Quality Inspection {doc.name} rejected.",
        }).insert(ignore_permissions=True)
    except Exception:
        logger.exception("Failed to create quality floor event for %s", doc.name)


def on_work_order_update(doc, method):
    """Sync active Work Order to linked IoT devices."""
    if doc.status not in ("In Process", "Completed", "Closed"):
        return
    try:
        workstations = [op.workstation for op in (doc.operations or []) if op.workstation]
        if not workstations:
            return

        devices = frappe.get_all(
            "IoT Device Registry",
            filters={"linked_workstation": ["in", workstations]},
            pluck="name",
        )
        for device in devices:
            _db_set_value("IoT Device Registry", device, "linked_work_order", doc.name)
    except Exception:
        logger.exception("Failed to sync work order %s to IoT devices", doc.name)


def check_production_lag():
    """Scheduled hourly check for production lag against configured threshold.

    Creates a Production Floor Event when a work order's completion percentage
    is below (100 - threshold) to avoid spamming one event per hour.
    """
    settings = frappe.get_single("Factory Configuration")
    threshold = flt(settings.production_lag_threshold_pct)
    if threshold <= 0:
        return
    if threshold is None:
        threshold = 20

    target_completion = 100 - threshold

    work_orders = frappe.get_all(
        "Work Order",
        filters={"status": "In Process", "docstatus": 1},
        fields=["name", "qty", "produced_qty", "planned_start_date"],
    )

    for wo in work_orders:
        planned = flt(wo.qty)
        if not planned:
            continue

        produced = flt(wo.produced_qty)
        completion_pct = (produced / planned) * 100

        if completion_pct < target_completion:
            existing = _db_exists(
                "Production Floor Event",
                {
                    "work_order": wo.name,
                    "event_type": "Line Stoppage",
                    "event_time": [">=", today()],
                },
            )
            if existing:
                continue

            frappe.get_doc({
                "doctype": "Production Floor Event",
                "event_type": "Line Stoppage",
                "severity": "Warning",
                "event_time": now(),
                "work_order": wo.name,
                "description": f"Production lag detected: {completion_pct:.1f}% completion vs planned {planned}.",
            }).insert(ignore_permissions=True)

    frappe.db.commit()


def cleanup_old_telemetry():
    """Daily scheduled task: delete Machine Telemetry Log rows older than retention days."""
    settings = frappe.get_single("Factory Configuration")
    retention_days = settings.telemetry_retention_days
    if retention_days is None:
        retention_days = 90
    retention_days = cint(retention_days)
    if retention_days <= 0:
        return

    cutoff = add_days(today(), -retention_days)
    try:
        rows = _db_sql(
            "DELETE FROM `tabMachine Telemetry Log` WHERE recorded_at < %s",
            cutoff,
        )
        frappe.db.commit()
        logger.info("Deleted %s old telemetry rows before %s", rows, cutoff)
    except Exception:
        logger.exception("Failed to clean up old telemetry rows")
        raise
