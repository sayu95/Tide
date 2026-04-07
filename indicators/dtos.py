from dataclasses import dataclass

@dataclass(frozen=True)
class BokInterestRateDto:
    """
    한국은행(BOK) API로부터 수신한 한국 금리 데이터 DTO
    """
    name: str          # 통계항목명 (예: 한국은행 기준금리)
    value: float       # 금리 값 (예: 3.50)
    unit: str          # 단위 (예: %)
    date: str          # 공시 일자 (예: 20240314)

    @classmethod
    def from_api_row(cls, row: dict):
        """
        API의 raw한 딕셔너리 데이터를 DTO 객체로 변환 (Factory Method)
        """
        return cls(
            name=row.get('STAT_NAME'),
            value=float(row.get('DATA_VALUE', 0)),
            unit=row.get('UNIT_NAME'),
            date=row.get('TIME')
        )