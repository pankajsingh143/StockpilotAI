from datetime import datetime
from pydantic import BaseModel

class FinancialStatement(BaseModel):
    period: datetime
    total_revenue: float | None = None
    gross_profit: float | None = None
    operating_income: float | None = None
    ebitda: float | None = None
    net_income: float | None = None
    basic_eps: float | None = None
    diluted_eps: float | None = None

