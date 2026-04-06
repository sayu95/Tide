import httpx
from datetime import datetime
from django.conf import settings

class EcosService:
    def __init__(self):
        self.api_key = settings.ECOS_API_KEY
        # httpx 클라이언트를 미리 생성해두면 여러 번 호출할 때 효율적입니다.
        self.client = httpx.Client(base_url="https://ecos.bok.or.kr")
