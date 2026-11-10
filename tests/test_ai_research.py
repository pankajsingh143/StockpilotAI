import pytest
from backend.models.ai_research import AIResearchResponse
from backend.models.financial_research import (
    FinancialResearchResult,
    RevenueAnalysis,
    ProfitabilityAnalysis,
    EarningsAnalysis
)
from backend.services.ai_research import AIResearchService


class MockOllamaClient:
    def generate(self, prompt: str, format=None) -> str:
        assert format is not None
        assert format["type"] == "object"
        assert "summary" in format["properties"]
        assert "RELIANCE.NS" in prompt
        assert "25.0" in prompt

        return """
        {
            "symbol": "RELIANCE.NS",
            "summary": "Revenue growth is positive.",
            "strengths": ["Revenue increased by 25%"],
            "risks": ["Profitability requires further investigation"]
        }
        """


def test_ai_research_interprets_financial_metrics():
    financial_result = FinancialResearchResult(
        symbol="RELIANCE.NS",
        revenue=RevenueAnalysis(
            current_revenue=1000.0,
            previous_revenue=800.0,
            growth_percentage=25.0,
        ),
    )

    service = AIResearchService(
        ollama_client=MockOllamaClient()
    )

    result = service.analyze(financial_result)

    assert isinstance(result, AIResearchResponse)
    assert result.symbol == "RELIANCE.NS"
    assert result.summary == "Revenue growth is positive."
    assert len(result.strengths) == 1
    assert len(result.risks) == 1


def test_ai_research_rejects_invalid_json():
    financial_result = FinancialResearchResult(
        symbol="RELIANCE.NS",
        revenue=RevenueAnalysis(
            current_revenue=1000.0,
            previous_revenue=800.0,
            growth_percentage=25.0,
        ),
    )

    class InvalidOllamaClient:
        def generate(self, prompt: str, format=None) -> str:
            return "This is not valid JSON"

    service = AIResearchService(
        ollama_client=InvalidOllamaClient()
    )

    with pytest.raises(ValueError):
        service.analyze(financial_result)
    def test_ai_research_overrides_model_generated_symbol():
        financial_result = FinancialResearchResult(
            symbol="RELIANCE.NS",
            revenue=RevenueAnalysis(
                current_revenue=1000.0,
                previous_revenue=800.0,
                growth_percentage=25.0,
            ),
        )

    class IncorrectSymbolClient:
        def generate(self, prompt: str, format=None) -> str:
            return """
            {
                "symbol": "📊",
                "summary": "Revenue is growing.",
                "strengths": ["Revenue growth is positive"],
                "risks": ["Profitability needs review"]
            }
            """

    service = AIResearchService(
        ollama_client=IncorrectSymbolClient()
    )

    result = service.analyze(financial_result)

    assert result.symbol == "RELIANCE.NS"

def test_ai_research_includes_all_financial_metrics():
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

    class InspectingOllamaClient:
        def generate(self, prompt: str, format=None) -> str:
            assert "30.0" in prompt
            assert "5.0" in prompt
            assert "9.09" in prompt

            return """
            {
                "symbol": "incorrect",
                "summary": "Revenue growth exceeds profit growth.",
                "strengths": ["Revenue growth is positive"],
                "risks": ["Profit growth is slower than revenue growth"]
            }
            """

    service = AIResearchService(
        ollama_client=InspectingOllamaClient()
    )

    result = service.analyze(financial_result)

    assert result.symbol == "RELIANCE.NS"