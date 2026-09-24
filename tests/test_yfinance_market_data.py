import pandas as pd

from datetime import datetime
from backend.repositories.financial_data import FinancialStatement
from backend.repositories.yfinance_market_data import (
    YFinanceMarketDataProvider,
)


class MockYFinanceClient:

    def get_data(self, symbol: str):
        return {
            "price": 1500.0,
            "market_cap": 1_000_000_000.0,
            
        }

    def get_income_statement(self, symbol: str):
        return pd.DataFrame(
            {
                pd.Timestamp("2026-03-31"): {
                    "Total Revenue": 1000000.0,
                    "Net Income": 100000.0,
                    "Gross Profit": 500000.0,
                    "Operating Income": 400000.0,
                    "EBITDA": 450000.0,
                    "Basic EPS": 1.0,
                    "Diluted EPS": 0.9
                },
                pd.Timestamp("2025-03-31"): {
                    "Total Revenue": 900000.0,
                    "Net Income": 90000.0,
                    "Gross Profit": 450000.0,
                    "Operating Income": 360000.0,
                    "EBITDA": 405000.0,
                    "Basic EPS": 1.0,
                    "Diluted EPS": 0.9  
                },
            }
        )

def test_yfinance_provider_maps_data_to_stock_market_data():

    client = MockYFinanceClient()

    provider = YFinanceMarketDataProvider(client)

    result = provider.get_stock_data("RELIANCE.NS")

    assert result.symbol == "RELIANCE.NS"
    assert result.price == 1500.0
    