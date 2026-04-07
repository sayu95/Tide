from django.shortcuts import render

# Create your views here.

# indicators/views.py
from .service.ecos_service import EcosService
from django.http import JsonResponse


# indicators/views.py
def sync_indicator_view(request):
    print("--- View Start ---")
    service = EcosService()

    code = request.GET.get('code', '722Y001')
    start = request.GET.get('start', '202301')
    end = request.GET.get('end', '202312')

    try:
        # 1. 서비스 호출
        result = service.fetch_and_save_interest_rate(code, start, end)

        # 2. 결과값 존재 여부 확인 (자바의 if (result != null) 과 동일)
        if result and result[0]:
            obj = result[0]
            return JsonResponse({
                "status": "success",
                "name": obj.name,
                "message": "Data saved successfully"
            }, status=200)  # 200을 명시적으로 넣어보세요.

        # 3. 데이터가 없는 경우
        return JsonResponse({"status": "error", "message": "No Data from BOK"}, status=200)

    except Exception as e:
        print(f"!!! CRITICAL ERROR: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)