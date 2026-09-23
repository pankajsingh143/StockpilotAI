from datetime import datetime
from fastapi.testclient import TestClient
from backend.api.dependencies import get_research_service
from backend.main import app
from backend.repositories.yfinance_market_data import StockMarketData

class MockResearchService:
    def get_stock_research(self, symbol: str) -> StockMarketData:
        return StockMarketData(
            symbol=symbol,
            price=1500.0,
            market_cap=1_000_000_000.0,
        )
def test_get_stock_research():  
    app.dependency_overrides[get_research_service] = lambda: MockResearchService()
    client = TestClient(app)
    response = client.get("/stocks/RELIANCE.NS/research")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "RELIANCE.NS"
    assert data["price"] == 1500.0
    assert data["market_cap"] == 1_000_000_000.0

    app.dependency_overrides.clear()  # Clear the override after the test