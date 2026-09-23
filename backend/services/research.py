from backend.repositories.market_data import (MarketDataProvider, 
                                              StockMarketData
)
class ResearchService:
    def __init__(self, market_data_provider: MarketDataProvider):
        self.market_data_provider = market_data_provider

    def get_stock_research(self, symbol: str) -> StockMarketData:
        return self.market_data_provider.get_stock_data(symbol)