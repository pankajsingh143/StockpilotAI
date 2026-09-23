import yfinance as yf

class  YFinanceClient:
    def get_data(self, symbol: str):
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
        }
    def get_income_statement(self, symbol: str):
        ticker = yf.Ticker(symbol)
        income_statement = ticker.income_stmt   
        return income_statement