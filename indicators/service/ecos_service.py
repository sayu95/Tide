import httpx
from django.conf import settings

from ..models import Indicator
from ..dtos import BokInterestRateDto

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

        # 1. API 경로 설정 및 호출
        path = f"/api/StatisticSearch/{self.api_key}/json/kr/1/1/{stat_code}/D/{start_date}/{end_date}"
        response = self.client.get(path)
        data = response.json()

        dto = BokInterestRateDto.from_api_row(data["StatisticSearch"]["row"][-1])

        # 3. DB 저장 (JPA의 save() 혹은 update_or_create() 역할)
        obj, created = Indicator.objects.update_or_create(
            code=stat_code,
            defaults={
                'name': dto.name,
                'value': dto.value,
                'unit': dto.unit,
                'date': dto.date
            }
        )
        return obj, created