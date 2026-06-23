import unittest
from unittest.mock import MagicMock, patch


class TestSyncApi(unittest.TestCase):
    def _call(self, func_name, request_json=None, args=None):
        with patch("frappe_factory.sync.api._get_api_key", return_value="secret"), \
             patch("frappe_factory.sync.api._check_rate_limit") as mock_rl, \
             patch("frappe_factory.sync.api.frappe") as mock_frappe:
            mock_frappe.request = MagicMock()
            mock_frappe.request.headers = {"X-OpsEdge-API-Key": "secret"}
            mock_frappe.request.get_json.return_value = request_json or {}
            mock_frappe.request.args = args or {}
            mock_frappe.utils.now.return_value = "2026-06-23 12:00:00"
            mock_frappe.as_json = lambda x: str(x)
            from frappe_factory.sync import api
            return getattr(api, func_name)()

    def test_get_pending_records_returns_records(self):
        with patch("frappe_factory.sync.api.frappe.get_all") as mock_get_all:
            mock_get_all.return_value = [{"name": "LOG-0001", "status": "Running"}]
            result = self._call("get_pending_records", args={"limit": "10"})
            self.assertEqual(result["records"][0]["name"], "LOG-0001")

    def test_get_pending_records_rejects_invalid_limit(self):
        with patch("frappe_factory.sync.api.frappe.get_all") as mock_get_all:
            mock_get_all.return_value = []
            with self.assertRaises(Exception):
                self._call("get_pending_records", args={"limit": "5000"})

    def test_mark_synced_rejects_missing_name(self):
        with self.assertRaises(Exception):
            self._call("mark_synced", request_json={})

    def test_mark_synced_updates_status(self):
        with patch("frappe_factory.sync.api.frappe.db.set_value") as mock_set, \
             patch("frappe_factory.sync.api.frappe.db.exists", return_value=True):
            result = self._call("mark_synced", request_json={"name": "LOG-0001"})
            mock_set.assert_called_with("OpsEdge Sync Log", "LOG-0001", "status", "Success")
            self.assertEqual(result["name"], "LOG-0001")

    def test_log_sync_result_inserts_doc(self):
        with patch("frappe_factory.sync.api.frappe.get_doc") as mock_get_doc:
            mock_doc = MagicMock()
            mock_doc.name = "LOG-0002"
            mock_get_doc.return_value = mock_doc
            result = self._call("log_sync_result", request_json={"status": "Success", "records_synced": 5})
            mock_doc.insert.assert_called_once()
            self.assertEqual(result["name"], "LOG-0002")

    def test_log_sync_result_rejects_invalid_status(self):
        with self.assertRaises(Exception):
            self._call("log_sync_result", request_json={"status": "Unknown"})
