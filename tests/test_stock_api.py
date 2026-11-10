from datetime import datetime
from fastapi.testclient import TestClient
from backend.api.dependencies import get_research_service
from backend.main import app
from backend.repositories.yfinance_market_data import StockMarketData

from backend.api.dependencies import (
    get_research_service,
    get_ai_research_service,
)
from backend.models.financial_research import (
    FinancialResearchResult,
    RevenueAnalysis,
    ProfitabilityAnalysis,
    EarningsAnalysis,
)
from backend.models.ai_research import AIResearchResponse

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

def test_get_ai_stock_research():
    
    financial_result = FinancialResearchResult(
        symbol="RELIANCE.NS",
        revenue=RevenueAnalysis(
            current_revenue=1300.0,
            previous_revenue=1000.0,
            growth_percentage=30.0,
        ),
        profitability=ProfitabilityAnalysis(
            net_profit=105.0,
            profit_growth_percentage=5.0,
            net_margin_percentage=8.1,
        ),
        earnings=EarningsAnalysis(
            current_eps=12.0,
            previous_eps=11.0,
            eps_growth_percentage=9.09,
        ),
    )

    class MockResearchService:
        def get_financial_research_result(self, symbol):
            assert symbol == "RELIANCE.NS"
            return financial_result

    class MockAIResearchService:
        def analyze(self, result):
            assert result == financial_result

            return AIResearchResponse(
                symbol=result.symbol,
                summary="Revenue growth exceeds profit growth.",
                strengths=["Revenue growth is 30%"],
                risks=["Profit growth is only 5%"],
                observations=[
                    "Revenue growth is 30%.",
                    "Profit growth is 5%.",
                ],
            )

    app.dependency_overrides[get_research_service] = (
        lambda: MockResearchService()
    )
    app.dependency_overrides[get_ai_research_service] = (
        lambda: MockAIResearchService()
    )
    client = TestClient(app)
    try:
        response = client.get("/stocks/RELIANCE.NS/ai-research")

        assert response.status_code == 200

        data = response.json()

        assert data["symbol"] == "RELIANCE.NS"
        assert data["summary"] == "Revenue growth exceeds profit growth."
        assert data["strengths"] == ["Revenue growth is 30%"]
        assert data["risks"] == ["Profit growth is only 5%"]
        assert data["observations"] == [
            "Revenue growth is 30%.",
            "Profit growth is 5%.",
        ]

    finally:
        app.dependency_overrides.clear()