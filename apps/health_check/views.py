from rest_framework.views import APIView
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class HealthCheck(APIView):

    def get(self, *args, **kwargs):
        logger.info('Information incoming!')
        return Response(
            {
                "status_code": 200,
                "detail": "ok",
                "result": "working"
            }
        )
