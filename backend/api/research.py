from fastapi import APIRouter
from backend.repositories.yfinance_market_data import YFinanceMarketDataProvider
from backend.repositories.yfinance_client import YFinanceClient
from backend.services.research import ResearchService

research_router = APIRouter(prefix="/stocks", tags=["Research"])

@research_router.get("/{symbol}/research")
def get_stock_research(symbol: str):
    yfinance_client = YFinanceClient()
    market_data_provider = YFinanceMarketDataProvider(yfinance_client)
    research_service = ResearchService(market_data_provider)

    stock_research = research_service.get_stock_research(symbol)
    return stock_research
