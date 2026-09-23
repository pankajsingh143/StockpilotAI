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