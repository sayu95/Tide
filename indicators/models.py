from django.db import models

# Create your models here.

class Indicator(models.Model):
    # 1. 지표 식별 코드 (ex: 한국은행 ECOS의 '010Y002')
    code = models.CharField(max_length=50, unique=True)

    # 2. 지표의 이름 (예: '국고채 3년', 소비자물가지수')
    name = models.CharField(max_length=100)

    # 3. 데이터의 단위 (예: %, 조원, 포인트)
    # default='%': 값이 입력되지 않으면 기본적으로 '%'가 들어감.
    unit = models.CharField(max_length=20, default='%')

    # 4. 데이터 수집 주기 (예: 일, 월, 분기, 년)
    # default='월': 한국은행 데이터는 월 단위가 많으므로 기본값을 '월'로 설정.
    period = models.CharField(max_length=10, default='월')

    # 5. 금리 숫자 저장 (실수형)
    value = models.FloatField(null=True, blank=True)

    # 6. # '202312' 같은 날짜 저장
    date = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        # 자바의 toString() 메서드와 동일한 역할.
        # 어드민 페이지나 로그에서 객체를 볼 때 'id' 대신 '이름'이 보이게 함.
        return self.name