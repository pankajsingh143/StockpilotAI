class YFinanceMarketDataProvider:
    def __init__(self, yfinance_client):
        self.yfinance_client = yfinance_client

    def get_stock_data(self, ticker):
        # Fetch market data using the yfinance client
        data = self.yfinance_client.get_data(ticker)
        return data