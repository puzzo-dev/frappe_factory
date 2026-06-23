import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch


class TestWebhookHelpers(unittest.TestCase):
    @contextmanager
    def _make_api(self):
        with patch("frappe_factory.iot.webhooks._get_webhook_token", return_value="secret"), \
             patch("frappe_factory.iot.webhooks._check_rate_limit"), \
             patch("frappe_factory.iot.webhooks._check_ip_allowed"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks._get_config") as mock_config, \
             patch("frappe_factory.iot.webhooks._get_request_json", return_value={}), \
             patch("frappe_factory.iot.webhooks._get_request_header", return_value="secret"), \
             patch("frappe_factory.iot.webhooks._db_get_value") as mock_db_get, \
             patch("frappe_factory.iot.webhooks._db_set_value") as mock_db_set, \
             patch("frappe_factory.iot.webhooks._db_exists") as mock_db_exists, \
             patch("frappe_factory.iot.webhooks._db_sql") as mock_db_sql, \
             patch("frappe_factory.iot.webhooks.frappe.get_doc") as mock_get_doc, \
             patch("frappe_factory.iot.webhooks.frappe.as_json", lambda x: str(x)), \
             patch("frappe_factory.iot.webhooks.frappe.enqueue") as mock_enqueue, \
             patch("frappe_factory.iot.webhooks.now", return_value="2026-06-23 12:00:00"):
            mock_config.return_value = MagicMock(
                enable_async_telemetry=0,
                enable_bulk_telemetry=0,
                enable_telemetry_dedup=0,
                production_lag_threshold_pct=20,
                telemetry_retention_days=90,
            )
            from frappe_factory.iot import webhooks
            webhooks.frappe.throw.side_effect = Exception("frappe.throw")
            yield webhooks

    def test_telemetry_requires_device_id(self):
        with self._make_api() as api:
            with self.assertRaises(Exception):
                api.telemetry()

    def test_telemetry_rejects_unknown_device(self):
        with self._make_api() as api:
            api._get_request_json.return_value = {"device_id": "unknown"}
            api._db_get_value.return_value = None
            with self.assertRaises(Exception):
                api.telemetry()

    def test_telemetry_skips_inactive_device(self):
        with self._make_api() as api:
            api._get_request_json.return_value = {"device_id": "dev-1", "values": {"temp": 22}}
            api._db_get_value.return_value = MagicMock(name="OED-0001", linked_workstation=None, is_active=0)
            result = api.telemetry()
            self.assertEqual(result["reason"], "device_inactive")

    def test_telemetry_inserts_records(self):
        with self._make_api() as api:
            api._get_request_json.return_value = {
                "device_id": "dev-1",
                "ts": 1719144000000,
                "values": {"temperature": 22.5, "status": "Running"},
            }
            device = MagicMock(name="OED-0001", linked_workstation=None, is_active=1)
            api._db_get_value.return_value = device
            mock_doc = MagicMock()
            api.frappe.get_doc.return_value = mock_doc
            result = api.telemetry()
            self.assertEqual(result["records"], 2)
            self.assertEqual(mock_doc.insert.call_count, 2)

    def test_telemetry_async_returns_queued(self):
        with self._make_api() as api:
            api._get_request_json.return_value = {"device_id": "dev-1", "values": {"temp": 22}}
            device = MagicMock(name="OED-0001", linked_workstation=None, is_active=1)
            api._db_get_value.return_value = device
            api._get_config.return_value = MagicMock(enable_async_telemetry=1)
            result = api.telemetry()
            self.assertEqual(result["status"], "queued")
            api.frappe.enqueue.assert_called_once()

    def test_parse_timestamp_handles_invalid(self):
        with self._make_api() as api:
            with self.assertRaises(Exception):
                api._parse_timestamp("not-a-number")

    def test_parse_metric_value_coerces_invalid(self):
        with self._make_api() as api:
            self.assertEqual(api._parse_metric_value("abc"), 0.0)
            self.assertEqual(api._parse_metric_value(42), 42.0)
            self.assertEqual(api._parse_metric_value(True), 1.0)

    def test_alarm_rejects_invalid_event_type(self):
        with self._make_api() as api:
            api._get_request_json.return_value = {"device_id": "dev-1", "event_type": "Bad"}
            api._db_get_value.return_value = MagicMock(name="OED-0001", linked_workstation=None)
            with self.assertRaises(Exception):
                api.alarm()

    def test_device_connected_updates_last_seen(self):
        with self._make_api() as api:
            api._get_request_json.return_value = {"device_id": "dev-1", "connected": True}
            api._db_get_value.return_value = MagicMock(name="OED-0001")
            result = api.device_connected()
            self.assertEqual(result["status"], "ok")
            api._db_set_value.assert_called_once()

    def test_health_check(self):
        with self._make_api() as api:
            result = api.health_check()
            self.assertEqual(result["status"], "ok")


class TestDocEventHooks(unittest.TestCase):
    def test_on_attendance_submit_updates_correct_fields(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks._db_get_value", return_value="SAS-2026-06-23-001"), \
             patch("frappe_factory.iot.webhooks.frappe.get_doc") as mock_get_doc, \
             patch("frappe_factory.iot.webhooks.logger"):
            summary = MagicMock()
            summary.total_present = 5
            summary.total_absent = 1
            mock_get_doc.return_value = summary
            from frappe_factory.iot.webhooks import on_attendance_submit

            doc = MagicMock()
            doc.employee = "EMP-001"
            doc.attendance_date = "2026-06-23"
            doc.status = "Present"
            doc.name = "ATT-001"
            on_attendance_submit(doc, "on_submit")
            self.assertEqual(summary.total_present, 6)
            summary.save.assert_called_once()

    def test_on_attendance_submit_no_summary_logs_and_returns(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks._db_get_value", return_value=None), \
             patch("frappe_factory.iot.webhooks.frappe.get_doc") as mock_get_doc, \
             patch("frappe_factory.iot.webhooks.logger"):
            from frappe_factory.iot.webhooks import on_attendance_submit

            doc = MagicMock()
            doc.employee = "EMP-001"
            doc.attendance_date = "2026-06-23"
            doc.status = "Absent"
            doc.name = "ATT-001"
            on_attendance_submit(doc, "on_submit")
            mock_get_doc.assert_not_called()

    def test_on_quality_submit_creates_event(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks._db_get_value", return_value=None), \
             patch("frappe_factory.iot.webhooks.frappe.get_doc") as mock_get_doc, \
             patch("frappe_factory.iot.webhooks.logger"), \
             patch("frappe_factory.iot.webhooks.now", return_value="2026-06-23 12:00:00"):
            from frappe_factory.iot.webhooks import on_quality_submit

            doc = MagicMock()
            doc.status = "Rejected"
            doc.name = "QI-001"
            doc.workstation = "WS-001"
            doc.reference_name = "WO-001"
            on_quality_submit(doc, "on_submit")
            mock_get_doc.assert_called_once()
            kwargs = mock_get_doc.call_args.kwargs
            if kwargs:
                self.assertEqual(kwargs["work_order"], "WO-001")
            else:
                self.assertEqual(mock_get_doc.call_args.args[0]["work_order"], "WO-001")

    def test_on_quality_submit_fetches_workstation_from_work_order(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks._db_get_value", return_value="WS-002"), \
             patch("frappe_factory.iot.webhooks.frappe.get_doc") as mock_get_doc, \
             patch("frappe_factory.iot.webhooks.logger"), \
             patch("frappe_factory.iot.webhooks.now", return_value="2026-06-23 12:00:00"):
            from frappe_factory.iot.webhooks import on_quality_submit

            doc = MagicMock()
            doc.status = "Rejected"
            doc.name = "QI-001"
            doc.workstation = None
            doc.reference_name = "WO-001"
            on_quality_submit(doc, "on_submit")
            kwargs = mock_get_doc.call_args.kwargs
            if kwargs:
                self.assertEqual(kwargs["linked_workstation"], "WS-002")
            else:
                self.assertEqual(mock_get_doc.call_args.args[0]["linked_workstation"], "WS-002")

    def test_on_work_order_update_links_devices(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks.frappe.get_all", return_value=["OED-0001", "OED-0002"]), \
             patch("frappe_factory.iot.webhooks.frappe.db.set_value") as mock_set, \
             patch("frappe_factory.iot.webhooks.logger"):
            from frappe_factory.iot.webhooks import on_work_order_update

            op1 = MagicMock(workstation="WS-001")
            op2 = MagicMock(workstation=None)
            doc = MagicMock()
            doc.status = "In Process"
            doc.operations = [op1, op2]
            doc.name = "WO-001"
            on_work_order_update(doc, "on_update")
            self.assertEqual(mock_set.call_count, 2)

    def test_on_work_order_update_ignores_non_active_status(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks.frappe.get_all") as mock_get_all, \
             patch("frappe_factory.iot.webhooks.logger"):
            from frappe_factory.iot.webhooks import on_work_order_update

            doc = MagicMock()
            doc.status = "Draft"
            on_work_order_update(doc, "on_update")
            mock_get_all.assert_not_called()


class TestCheckProductionLag(unittest.TestCase):
    def test_check_production_lag_creates_event(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks.frappe.get_single") as mock_single, \
             patch("frappe_factory.iot.webhooks.frappe.get_all") as mock_get_all, \
             patch("frappe_factory.iot.webhooks._db_exists", return_value=False), \
             patch("frappe_factory.iot.webhooks.frappe.get_doc") as mock_get_doc, \
             patch("frappe_factory.iot.webhooks.frappe.db.commit"), \
             patch("frappe_factory.iot.webhooks.now", return_value="2026-06-23 12:00:00"), \
             patch("frappe_factory.iot.webhooks.today", return_value="2026-06-23"):
            mock_single.return_value = MagicMock(production_lag_threshold_pct=20)
            mock_get_all.return_value = [
                MagicMock(name="WO-001", qty=100, produced_qty=50)
            ]
            mock_doc = MagicMock()
            mock_get_doc.return_value = mock_doc
            from frappe_factory.iot.webhooks import check_production_lag

            check_production_lag()
            mock_doc.insert.assert_called_once()

    def test_check_production_lag_disabled_when_threshold_zero(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks.frappe.get_single") as mock_single, \
             patch("frappe_factory.iot.webhooks.frappe.get_all") as mock_get_all, \
             patch("frappe_factory.iot.webhooks.now", return_value="2026-06-23 12:00:00"):
            mock_single.return_value = MagicMock(production_lag_threshold_pct=0)
            from frappe_factory.iot.webhooks import check_production_lag

            check_production_lag()
            mock_get_all.assert_not_called()


class TestCleanupOldTelemetry(unittest.TestCase):
    def test_cleanup_old_telemetry_deletes_rows(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks.frappe.get_single") as mock_single, \
             patch("frappe_factory.iot.webhooks._db_sql") as mock_sql, \
             patch("frappe_factory.iot.webhooks.frappe.db.commit"), \
             patch("frappe_factory.iot.webhooks.today", return_value="2026-06-23"), \
             patch("frappe_factory.iot.webhooks.add_days", return_value="2026-05-24"):
            mock_single.return_value = MagicMock(telemetry_retention_days=30)
            from frappe_factory.iot.webhooks import cleanup_old_telemetry

            cleanup_old_telemetry()
            mock_sql.assert_called_once()

    def test_cleanup_old_telemetry_disabled_when_retention_zero(self):
        with patch("frappe_factory.iot.webhooks._run_as_system_user"), \
             patch("frappe_factory.iot.webhooks._log_audit"), \
             patch("frappe_factory.iot.webhooks.frappe.get_single") as mock_single, \
             patch("frappe_factory.iot.webhooks._db_sql") as mock_sql, \
             patch("frappe_factory.iot.webhooks.today", return_value="2026-06-23"):
            mock_single.return_value = MagicMock(telemetry_retention_days=0)
            from frappe_factory.iot.webhooks import cleanup_old_telemetry

            cleanup_old_telemetry()
            mock_sql.assert_not_called()
