from backend.models.financial_research import (
    EarningsAnalysis,
    FinancialResearchResult,
    ProfitabilityAnalysis,
    RevenueAnalysis,
)
from backend.services.ai_research_prompt_builder import AIResearchPromptBuilder


def test_build_prompt_includes_symbol_and_all_financial_metrics():
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

    prompt = AIResearchPromptBuilder().build_prompt(financial_result)

    assert "Stock: RELIANCE.NS" in prompt
    assert "current_revenue" in prompt
    assert "1300.0" in prompt
    assert "profit_growth_percentage" in prompt
    assert "5.0" in prompt
    assert "eps_growth_percentage" in prompt
    assert "9.09" in prompt
    assert '"symbol": "RELIANCE.NS"' in prompt


def test_build_prompt_marks_missing_metrics_as_unavailable():
    financial_result = FinancialResearchResult(symbol="RELIANCE.NS")

    prompt = AIResearchPromptBuilder().build_prompt(financial_result)

    assert "Revenue analysis:\nNot available" in prompt
    assert "Profitability analysis:\nNot available" in prompt
    assert "Earnings analysis:\nNot available" in prompt


def test_build_prompt_is_cleanly_formatted_and_contains_json_instructions():
    financial_result = FinancialResearchResult(symbol="RELIANCE.NS")

    prompt = AIResearchPromptBuilder().build_prompt(financial_result)

    assert prompt.startswith("You are a financial research analyst.")
    assert prompt.endswith("}")
    assert "Return only valid JSON in this exact structure:" in prompt
    assert "Do not provide buy or sell recommendations." in prompt
