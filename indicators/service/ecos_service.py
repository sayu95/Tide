import httpx
from django.conf import settings

class EcosService:
    def __init__(self):
        # 자바의 생성자(@Autowired 필드 주입 등)와 같은 역할입니다.
        # 여기서 self.api_key를 만들어줘야 아래 메서드에서 쓸 수 있습니다.
        self.api_key = settings.ECOS_API_KEY
        self.client = httpx.Client(base_url="https://ecos.bok.or.kr")

    def fetch_and_save_interest_rate(self, stat_code, start_date, end_date):
        """
        한국은행 API를 통해 금리 지표를 수집하고 DB에 저장합니다.
        Args:
            stat_code (str): 통계 코드 (예: '722Y001')
            start_date (str): 시작 날짜 (YYYYMMDD)
            ...
        Returns:
            tuple: (Indicator 객체, 생성 여부 Boolean)
        """
        # 1. API 호출 (기존 메서드를 인라인으로 합침)
        path = f"/api/StatisticSearch/{self.api_key}/json/kr/1/1/{stat_code}/D/{start_date}/{end_date}/?"
        response = self.client.get(path)

        # 디버깅용 로그 (필요없으면 삭제 가능)
        print(f"DEBUG URL: {response.url}")

        data = response.json()

        # 2. 에러 메시지 여부 확인
        if "RESULT" in data:
            print(f"!!! BOK API Message: {data['RESULT'].get('message')}")
            return None, False

        # 3. 데이터 추출
        search_data = data.get("StatisticSearch", {})
        rows = search_data.get("row", [])

        if not rows:
            print(f"!!! No row data found for {stat_code}")
            return None, False

        latest_data = rows[-1]  # 가장 최근 데이터

        # 4. DB 저장 (JPA의 save() 혹은 merge()와 유사)
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