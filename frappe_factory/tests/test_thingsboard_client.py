import unittest
from unittest.mock import MagicMock, patch


class TestThingsBoardClient(unittest.TestCase):
    def _make_client(self, url="http://tb.local:8080", token="abc"):
        with patch("frappe_factory.iot.thingsboard.frappe.get_single") as mock_single:
            settings = MagicMock()
            settings.thingsboard_url = url
            settings.get_password.return_value = token
            mock_single.return_value = settings
            from frappe_factory.iot.thingsboard import ThingsBoardClient
            return ThingsBoardClient()

    def test_headers_contain_bearer_token(self):
        client = self._make_client()
        self.assertEqual(client.headers["X-Authorization"], "Bearer abc")

    @patch("frappe_factory.iot.thingsboard.requests.get")
    def test_get_telemetry_calls_timeseries_endpoint(self, mock_get):
        mock_get.return_value.json.return_value = {"temperature": [{"ts": 1, "value": 22}]}
        mock_get.return_value.text = '{"temperature": []}'
        mock_get.return_value.raise_for_status = MagicMock()
        client = self._make_client()
        result = client.get_telemetry("dev-1", keys=["temperature"])
        self.assertIn("temperature", result)
        mock_get.assert_called_once()

    @patch("frappe_factory.iot.thingsboard.requests.post")
    def test_send_attributes_calls_server_scope_endpoint(self, mock_post):
        mock_post.return_value.json.return_value = {}
        mock_post.return_value.text = ""
        mock_post.return_value.raise_for_status = MagicMock()
        client = self._make_client()
        client.send_attributes("dev-1", {"job_card_paused": True})
        url = mock_post.call_args[0][0]
        self.assertIn("/api/plugins/telemetry/DEVICE/dev-1/attributes/SERVER_SCOPE", url)
