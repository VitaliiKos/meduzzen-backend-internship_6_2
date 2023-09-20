from rest_framework.views import APIView
from rest_framework.response import Response


class HealthCheck(APIView):
    def get(self, *args, **kwargs):
        return Response(
            {
                "status_code": 200,
                "detail": "ok",
                "result": "working"
            }
        )
