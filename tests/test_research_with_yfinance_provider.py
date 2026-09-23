from datetime import datetime

from backend.repositories.yfinance_market_data import (
    YFinanceMarketDataProvider,
)
from backend.services.research import ResearchService


class MockYFinanceClient:

    def get_data(self, symbol: str):
        return {
            "price": 1500.0,
            "market_cap": 1_000_000_000.0,
            "pe_ratio": 25.0,
            "revenue": 500_000_000.0,
            "earnings": 50_000_000.0,
            "as_of_date": datetime.now(),
        }


def test_research_service_with_yfinance_provider():

    client = MockYFinanceClient()

    provider = YFinanceMarketDataProvider(client)

    research_service = ResearchService(
        market_data_provider=provider
    )

    result = research_service.get_stock_research(
        "RELIANCE.NS"
    )

    assert result.symbol == "RELIANCE.NS"
    assert result.price == 1500.0
   