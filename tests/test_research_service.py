from datetime import datetime

from backend.repositories.market_data import StockMarketData
from backend.services.research import ResearchService

class MockMarketDataProvider:
    def get_stock_data(self, symbol: str) -> StockMarketData:
        # Return mock data for testing purposes
        return StockMarketData(
            symbol=symbol,
            price=100.0,
            market_cap=1_000_000_000.0,
            pe_ratio=15.0,
            revenue=500_000_000.0,
            earnings=50_000_000.0,
            as_of_date=datetime.now()
        )

def test_research_service_with_mock_data():
    # Create a mock market data provider
    mock_provider = MockMarketDataProvider()
    
    # Create an instance of the ResearchService with the mock provider
    research_service = ResearchService(market_data_provider=mock_provider)
    
    result = research_service.get_stock_research("RELIANCE.NS")
    # Assert that the result matches the mock data
    assert result.symbol == "RELIANCE.NS"
    assert result.price == 100.0
    assert result.market_cap == 1_000_000_000.0
    assert result.pe_ratio == 15.0
    assert result.revenue == 500_000_000.0
    assert result.earnings == 50_000_000.0
    assert isinstance(result.as_of_date, datetime)      