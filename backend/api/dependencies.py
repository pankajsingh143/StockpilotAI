from backend.repositories.yfinance_market_data import YFinanceMarketDataProvider
from backend.repositories.yfinance_client import YFinanceClient
from backend.services.research import ResearchService

def get_research_service() -> ResearchService:
    yfinance_client = YFinanceClient()
    market_data_provider = YFinanceMarketDataProvider(yfinance_client)
    return ResearchService(market_data_provider)