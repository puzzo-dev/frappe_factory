"""Webhook receivers for ThingsBoard and ERPNext document events.

ThingsBoard HTTP Integration posts to:
    https://<site>/api/method/frappe_factory.iot.webhooks.<method_name>

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
    """Receive telemetry payload from ThingsBoard.

    Payload should contain at minimum:
        device_id: ThingsBoard device ID
        ts: Unix timestamp (ms)
        values: dict of metric key -> value
    """
    _validate_webhook_token()
    data = frappe.request.get_json() or {}
    tb_device_id = data.get("device_id")
    if not tb_device_id:
        frappe.throw("device_id is required", frappe.MandatoryError)

    device = frappe.db.get_value(
        "IoT Device Registry",
        {"thingsboard_device_id": tb_device_id},
        ["name", "linked_workstation", "is_active"],
        as_dict=True,
    )
    if not device:
        frappe.throw(f"Unknown device {tb_device_id}", frappe.DoesNotExistError)

    if not device.is_active:
        return {"status": "skipped", "reason": "device_inactive"}

    values = data.get("values", {})
    ts = data.get("ts")
    recorded_at = frappe.utils.format_datetime(frappe.utils.get_datetime(ts / 1000)) if ts else frappe.utils.now()

    for metric_key, metric_value in values.items():
        _insert_telemetry(device, tb_device_id, metric_key, metric_value, recorded_at, data)

    if device.linked_workstation:
        _update_workstation_status(device.linked_workstation, values)

    frappe.db.commit()
    return {"status": "ok", "records": len(values)}


def _insert_telemetry(device, tb_device_id, metric_key, metric_value, recorded_at, raw_payload):
    try:
        metric_float = float(metric_value)
    except (ValueError, TypeError):
        metric_float = 0.0

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
    frappe.db.set_value("Workstation", workstation_name, "status", status)


@frappe.whitelist(allow_guest=True, methods=["POST"])
def alarm():
    """Receive alarm payload from ThingsBoard."""
    _validate_webhook_token()
    data = frappe.request.get_json() or {}
    tb_device_id = data.get("device_id")
    if not tb_device_id:
        frappe.throw("device_id is required", frappe.MandatoryError)

    device = frappe.db.get_value(
        "IoT Device Registry",
        {"thingsboard_device_id": tb_device_id},
        ["name", "linked_workstation"],
        as_dict=True,
    )
    if not device:
        frappe.throw(f"Unknown device {tb_device_id}", frappe.DoesNotExistError)

    frappe.get_doc({
        "doctype": "Production Floor Event",
        "event_type": data.get("event_type", "Machine Fault"),
        "severity": data.get("severity", "Critical"),
        "event_time": frappe.utils.now(),
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
    data = frappe.request.get_json() or {}
    tb_device_id = data.get("device_id")
    connected = data.get("connected", True)
    if not tb_device_id:
        frappe.throw("device_id is required", frappe.MandatoryError)

    device_name = frappe.db.get_value(
        "IoT Device Registry",
        {"thingsboard_device_id": tb_device_id},
        "name",
    )
    if not device_name:
        frappe.throw(f"Unknown device {tb_device_id}", frappe.DoesNotExistError)

    frappe.db.set_value("IoT Device Registry", device_name, "last_seen", frappe.utils.now())
    frappe.db.commit()
    return {"status": "ok", "device": device_name, "connected": connected}


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
    settings = frappe.get_single("Factory Configuration")
    threshold = settings.production_lag_threshold_pct or 20
    # TODO: compare planned vs actual output and trigger n8n alert
    pass
