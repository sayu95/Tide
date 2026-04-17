# indicators/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .decorators import handle_view_exceptions
from .service.ecos_service import EcosService

@api_view(['GET'])
@handle_view_exceptions
def sync_indicator_view(request):
    service = EcosService()

    # 1. 1999년부터 전수 조사를 수행하는 서비스 메서드 호출
    # 이 메서드는 내부적으로 19990507 ~ 오늘까지를 긁어오도록 짜여 있습니다.
    total, saved = service.fetch_all_base_rate_history()

    # 2. 결과 리턴
    return Response({
        "status": "SUCCESS",
        "payload": {
            "total_count": total,
            "newly_saved_count": saved,
            "message": "1999년 제공일부터 오늘까지 전수 동기화 완료"
        }
    })