from rest_framework.test import APITestCase


class HealthCheckTestCase(APITestCase):
    """Test case for the health check endpoint."""

    def test_health_check_endpoint(self):
        """Test the health check endpoint."""
        response = self.client.get('/health_check')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status_code": 200, "detail": "ok", "result": "working"})
