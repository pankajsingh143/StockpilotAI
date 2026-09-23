from datetime import datetime

from backend.repositories.yfinance_market_data import (
    YFinanceMarketDataProvider,
)


class MockYFinanceClient:

    def get_data(self, symbol: str):
        return {
            "price": 1500.0,
            "market_cap": 1_000_000_000.0,
            
        }


def test_yfinance_provider_maps_data_to_stock_market_data():

    client = MockYFinanceClient()

    provider = YFinanceMarketDataProvider(client)

    result = provider.get_stock_data("RELIANCE.NS")

    assert result.symbol == "RELIANCE.NS"
    assert result.price == 1500.0
    