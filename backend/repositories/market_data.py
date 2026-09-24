from datetime import datetime
from typing import Protocol
from pydantic import BaseModel
from backend.repositories.financial_data import FinancialStatement

class StockMarketData(BaseModel):
    symbol: str
    price: float | None = None
    market_cap: float | None = None
    pe_ratio: float | None = None
    revenue: float | None = None
    earnings: float | None = None
    as_of_date: datetime | None = None

class MarketDataProvider(Protocol):
    def get_stock_data(self, symbol: str) -> StockMarketData:
        ...
    def get_financial_statements(self, symbol: str) -> list[FinancialStatement]:
        ... 