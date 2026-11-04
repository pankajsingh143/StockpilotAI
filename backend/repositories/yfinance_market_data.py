import pandas as pd
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
        income_statements = self.yfinance_client.get_income_statement(symbol)
        statements = []

        for period in income_statements.columns:

            def get_value(row: str) -> float | None:
                if row not in income_statements.index:
                    return None

                value = income_statements.loc[row, period]

                if pd.isna(value):
                    return None

                return float(value)

            statements.append(
                FinancialStatement(
                    period=period.to_pydatetime(),
                    total_revenue=get_value("Total Revenue"),
                    gross_profit=get_value("Gross Profit"),
                    operating_income=get_value("Operating Income"),
                    ebitda=get_value("EBITDA"),
                    net_income=get_value("Net Income"),
                    basic_eps=get_value("Basic EPS"),
                    diluted_eps=get_value("Diluted EPS"),
                )
            )

        return statements