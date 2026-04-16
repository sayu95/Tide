import httpx

from datetime import datetime
from django.conf import settings
from ..models import Indicator
from ..dtos import BokInterestRateDto

class EcosService:
    def __init__(self):
        # 자바의 생성자(@Autowired 필드 주입 등)와 같은 역할입니다.
        # 여기서 self.api_key를 만들어줘야 아래 메서드에서 쓸 수 있습니다.
        self.api_key = settings.ECOS_API_KEY
        self.client = httpx.Client(base_url="https://ecos.bok.or.kr")


    def fetch_and_save_indicator(self, stat_code, start_date, end_date, item_code):
        # 1. API 경로 설정 (1/50000으로 범위를 넉넉히 잡습니다)
        path = f"/api/StatisticSearch/{self.api_key}/json/kr/1/50000/{stat_code}/D/{start_date}/{end_date}/{item_code}"

        response = self.client.get(path)
        data = response.json()

        if "StatisticSearch" not in data:
            print(f"!!! Error from BOK: {data}")
            return 0, 0

        rows = data["StatisticSearch"]["row"]
        total_count = len(rows)
        saved_count = 0

        # 2. 루프 돌며 저장 (자바의 for-each 문과 동일)
        for row in rows:
            dto = BokInterestRateDto.from_api_row(row)

            # unique_together 덕분에 중복 걱정 없이 Upsert 가능!
            obj, created = Indicator.objects.update_or_create(
                code=stat_code,
                date=dto.date,
                defaults={
                    'name': dto.name,
                    'value': dto.value,
                    'unit': dto.unit,
                    'period': '일',  # 기준금리는 일별 데이터로 수집
                }
            )
            if created:
                saved_count += 1

        print(f"--- [SYNC COMPLETE] Total: {total_count}, Newly Saved: {saved_count} ---")
        return total_count, saved_count


    # [Helper] 기준금리 전수 수집용
    # indicators/service/ecos_service.py

    def fetch_all_base_rate_history(self):
        """
        1999년부터 현재까지의 모든 기준금리 데이터를 강제로 다 긁어옵니다.
        """
        stat_code = "722Y001"  # 기준금리
        item_code = "0101000"  # 한국은행 기준금리
        start_date = "19990507"  # 최초 제공일
        end_date = datetime.now().strftime('%Y%m%d')  # 오늘 날짜 (20260416)

        # 1번부터 50000번까지 요청 (전수 수집을 위해 범위를 크게 잡음)
        return self.fetch_and_save_indicator(stat_code, start_date, end_date, item_code)