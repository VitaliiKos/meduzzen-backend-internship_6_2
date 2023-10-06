import logging

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class HealthCheck(APIView):
    """A view for performing health checks."""

    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        """Handle GET request for health check."""
        logger.info('Information incoming!')
        return Response(
            {
                "status_code": 200,
                "detail": "ok",
                "result": "working"
            }
        )
