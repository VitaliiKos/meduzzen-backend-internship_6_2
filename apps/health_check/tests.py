from rest_framework.test import APITestCase


class HealthCheckTestCase(APITestCase):
    def test_health_check_endpoint(self):
        response = self.client.get('/health_check')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status_code": 200, "detail": "ok", "result": "working"})
