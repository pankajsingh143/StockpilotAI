from backend.repositories.yfinance_market_data import YFinanceMarketDataProvider
from backend.repositories.yfinance_client import YFinanceClient
from backend.services.research import ResearchService
from backend.repositories.ollama_client import OllamaClient
from backend.utils.config import settings

def get_research_service() -> ResearchService:
    yfinance_client = YFinanceClient()
    market_data_provider = YFinanceMarketDataProvider(yfinance_client)
    return ResearchService(market_data_provider)

def get_ollama_client() -> OllamaClient:
    return OllamaClient(base_url=settings.ollama_base_url, model=settings.ollama_model) 
