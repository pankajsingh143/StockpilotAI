import pandas as pd
from backend.repositories.yfinance_client import YFinanceClient

class MockTicker:
    @property
    def income_stmt(self):
        return pd.DataFrame(
            {
                pd.Timestamp("2026-03-31"): {
                    "Total Revenue": 1000000.0,
                    "Net Income": 100000.0,
                },
                pd.Timestamp("2025-03-31"): {
                    "Total Revenue": 900000.0,
                    "Net Income": 90000.0,
                },
            }
        )
def test_get_income_statement(monkeypatch):
    monkeypatch.setattr(
        "backend.repositories.yfinance_client.yf.Ticker", 
        lambda symbol: MockTicker()
    )
    client = YFinanceClient()
    result = client.get_income_statement("RELIANCE.NS")
    assert isinstance(result, pd.DataFrame)
    assert result.loc["Total Revenue", pd.Timestamp("2026-03-31")] == 1000000.0
    assert result.loc["Net Income", pd.Timestamp("2025-03-31")] == 90000.0
    