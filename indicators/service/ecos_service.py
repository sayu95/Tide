import httpx
from django.conf import settings

class EcosService:
    def __init__(self):
        # 자바의 생성자(@Autowired 필드 주입 등)와 같은 역할입니다.
        # 여기서 self.api_key를 만들어줘야 아래 메서드에서 쓸 수 있습니다.
        self.api_key = settings.ECOS_API_KEY
        self.client = httpx.Client(base_url="https://ecos.bok.or.kr")


    def sync_indicator(self, stat_code, start_date, end_date):
        response = self._fetch_ecos_data(stat_code, start_date, end_date)
        data = response.json()

        # 1. 에러 메시지 여부 확인
        if "RESULT" in data:
            print(f"!!! BOK API Message: {data['RESULT'].get('message')}")
            return None, False

        # 2. 데이터 추출
        search_data = data.get("StatisticSearch", {})
        rows = search_data.get("row", [])

        if not rows:
            print(f"!!! No row data found for {stat_code}")
            return None, False

        latest_data = rows[-1]  # 가장 최근 데이터

        # 3. DB 저장 (필드명 대문자 주의!)
        from ..models import Indicator
        obj, created = Indicator.objects.update_or_create(
            code=stat_code,
            defaults={
                'name': latest_data.get('STAT_NAME'),
                'value': latest_data.get('DATA_VALUE'),
                'unit': latest_data.get('UNIT_NAME'),
                'date': latest_data.get('TIME')
            }
        )
        return obj, created


    def _fetch_ecos_data(self, stat_code, start_date, end_date):
        path = (
            f"/api/StatisticSearch/{self.api_key}/json/kr/1/1/"
            f"{stat_code}/D/{start_date}/{end_date}/?"
        )

        response = self.client.get(path)
        print(f"DEBUG URL: {response.url}")  # 아까 터미널에 이건 잘 찍혔죠?

        # ★ 이게 빠져있을 겁니다! ★
        return response