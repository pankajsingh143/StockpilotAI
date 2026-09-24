from backend.repositories.financial_data import FinancialStatement
from backend.repositories.market_data import StockMarketData
from backend.repositories.yfinance_client import YFinanceClient


class YFinanceMarketDataProvider:
    def __init__(self, yfinance_client):
        self.yfinance_client = yfinance_client

    def get_stock_data(self, symbol: str) -> StockMarketData:
        # Fetch market data using the yfinance client
        data = self.yfinance_client.get_data(symbol)
        return StockMarketData(
            symbol=symbol,
            price=data.get("price"),
            market_cap=data.get("market_cap")
        )

    def get_financial_statements(self, symbol: str) -> list[FinancialStatement]:
        # Fetch financial statements using the yfinance client
        income_statements = self.yfinance_client.get_financial_statements(symbol)
        statements = []
        for period in income_statements.columns:
            statements.append(
                FinancialStatement(
                    period=period.to_pydatetime(),
                    total_revenue=income_statements.loc["Total Revenue", period],
                    gross_profit=income_statements.loc.get("Gross Profit", {}).get(period),
                    operating_income=income_statements.loc.get("Operating Income", {}).get(period),
                    ebitda=income_statements.loc.get("EBITDA", {}).get(period),
                    net_income=income_statements.loc["Net Income", period],
                    basic_eps=income_statements.loc.get("Basic EPS", {}).get(period),
                    diluted_eps=income_statements.loc.get("Diluted EPS", {}).get(period),
                )       
            )
        return statements