from backend.repositories.market_data import StockMarketData


class YFinanceMarketDataProvider:
    def __init__(self, yfinance_client):
        self.yfinance_client = yfinance_client

    def get_stock_data(self, symbol: str) -> StockMarketData:
        # Fetch market data using the yfinance client
        data = self.yfinance_client.get_data(symbol)
        return StockMarketData(
            symbol=symbol,
            price=data.get("price"),
            market_cap=data.get("market_cap"),
            pe_ratio=data.get("pe_ratio"),
            revenue=data.get("revenue"),
            earnings=data.get("earnings"),
            as_of_date=data.get("as_of_date")
        )