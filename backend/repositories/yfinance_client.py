import yfinance as yf

class  YFinanceClient:
    def get_data(self, symbol: str):
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
        }