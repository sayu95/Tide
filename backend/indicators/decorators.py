from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import httpx
import logging

logger = logging.getLogger(__name__)

def handle_view_exceptions(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except httpx.HTTPError as e:
            return Response({"status": "API_ERROR", "message": "한국은행 API 통신 실패"}, status=502)
        except Exception as e:
            logger.error(f"Critical System Error: {str(e)}")
            return Response({"status": "SYSTEM_ERROR", "message": str(e)}, status=500)
    return wrapper