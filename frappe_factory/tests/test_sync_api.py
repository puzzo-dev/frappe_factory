import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch


class TestSyncApi(unittest.TestCase):
    @contextmanager
    def _make_api(self, request_json=None, args=None):
        """Yield a mocked api module ready for testing."""
        with patch("frappe_factory.sync.api._get_api_key", return_value="secret"), \
             patch("frappe_factory.sync.api._check_rate_limit"), \
             patch("frappe_factory.sync.api._check_ip_allowed"), \
             patch("frappe_factory.sync.api._log_sync"), \
             patch("frappe_factory.sync.api._get_request_header", return_value="secret"), \
             patch("frappe_factory.sync.api._get_request_json", return_value=request_json or {}), \
             patch("frappe_factory.sync.api._get_request_args", return_value=args or {}):
            mock_frappe = MagicMock()
            mock_frappe.utils.now.return_value = "2026-06-23 12:00:00"
            mock_frappe.as_json = lambda x: str(x)
            mock_frappe.throw.side_effect = Exception("frappe.throw")
            with patch("frappe_factory.sync.api.frappe", mock_frappe):
                from frappe_factory.sync import api
                yield api

    def test_get_pending_records_returns_records(self):
        with self._make_api(args={"limit": "10"}) as api:
            api.frappe.get_all.return_value = [{"name": "LOG-0001", "status": "Running"}]
            result = api.get_pending_records()
            self.assertEqual(result["records"][0]["name"], "LOG-0001")

    def test_get_pending_records_rejects_invalid_limit(self):
        with self._make_api(args={"limit": "5000"}) as api:
            api.frappe.get_all.return_value = []
            with self.assertRaises(Exception):
                api.get_pending_records()

    def test_mark_synced_rejects_missing_name(self):
        with self._make_api(request_json={}) as api:
            with self.assertRaises(Exception):
                api.mark_synced()

    def test_mark_synced_updates_status(self):
        with self._make_api(request_json={"name": "LOG-0001"}) as api:
            api.frappe.db.exists.return_value = True
            result = api.mark_synced()
            api.frappe.db.set_value.assert_called_with("OpsEdge Sync Log", "LOG-0001", "status", "Success")
            self.assertEqual(result["name"], "LOG-0001")

    def test_mark_synced_rejects_unknown_record(self):
        with self._make_api(request_json={"name": "LOG-0001"}) as api:
            api.frappe.db.exists.return_value = False
            with self.assertRaises(Exception):
                api.mark_synced()

    def test_log_sync_result_inserts_doc(self):
        with self._make_api(request_json={"status": "Success", "records_synced": 5}) as api:
            mock_doc = MagicMock()
            mock_doc.name = "LOG-0002"
            api.frappe.get_doc.return_value = mock_doc
            result = api.log_sync_result()
            mock_doc.insert.assert_called_once()
            self.assertEqual(result["name"], "LOG-0002")

    def test_log_sync_result_rejects_invalid_status(self):
        with self._make_api(request_json={"status": "Unknown"}) as api:
            with self.assertRaises(Exception):
                api.log_sync_result()

    def test_log_sync_result_rejects_invalid_direction(self):
        with self._make_api(request_json={"sync_direction": "Up"}) as api:
            with self.assertRaises(Exception):
                api.log_sync_result()
