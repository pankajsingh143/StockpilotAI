from datetime import datetime

import pytest
from backend.repositories.financial_data import FinancialStatement
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

def test_calculate_revenue_analysis():
    service = ResearchService(MockMarketDataProvider())
    statements = [
        FinancialStatement(period=datetime(2025, 3, 31), total_revenue=1000000.0),
        FinancialStatement(period=datetime(2024, 3, 31), total_revenue=800000.0),
    ]
    result = service.calculate_revenue_analysis(statements)

    assert result.current_revenue == 1000000.0
    assert result.previous_revenue == 800000.0
    assert result.growth_percentage == 25.0  # ((1000000 - 800000) / 800000) * 100  

def test_revenue_analysis_with_insufficient_statements():
    service = ResearchService(MockMarketDataProvider())

    statements = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            total_revenue=1000000.0,
        )
    ]

    result = service.calculate_revenue_analysis(statements)

    assert result.growth_percentage is None


def test_revenue_analysis_with_zero_previous_revenue():
    service = ResearchService(MockMarketDataProvider())

    statements = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            total_revenue=0.0,
        ),
    ]

    result = service.calculate_revenue_analysis(statements)

    assert result.current_revenue == 1000000.0
    assert result.previous_revenue == 0.0
    assert result.growth_percentage is None


def test_revenue_analysis_with_missing_revenue():
    service = ResearchService(MockMarketDataProvider())

    statements = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            total_revenue=None,
        ),
    ]

    result = service.calculate_revenue_analysis(statements)

    assert result.growth_percentage is None

# add a method to test calculate_profitability_analysis with various scenarios, including missing data, zero previous net income, and valid data.
def test_calculate_profitability_analysis_with_various_scenarios():
    service = ResearchService(MockMarketDataProvider())

    # Test with valid data
    statements_valid = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            net_income=200000.0,
            operating_income=300000.0,
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            net_income=150000.0,
            operating_income=250000.0,
            total_revenue=800000.0,
        ),
    ]

    result_valid = service.calculate_profitability_analysis(statements_valid)

    assert result_valid.net_profit == 200000.0
    assert result_valid.profit_growth_percentage == 33.33333333333333  # ((200000 - 150000) / 150000) * 100
    assert result_valid.operating_margin_percentage == 30.0  # (300000 / 1000000) * 100
    assert result_valid.net_margin_percentage == 20.0  # (200000 / 1000000) * 100

    # Test with missing data
    statements_missing = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            net_income=None,
            operating_income=None,
            total_revenue=None,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            net_income=None,
            operating_income=None,
            total_revenue=None,
        ),
    ]

    result_missing = service.calculate_profitability_analysis(statements_missing)

    assert result_missing.net_profit is None
    assert result_missing.profit_growth_percentage is None
    assert result_missing.operating_margin_percentage is None
    assert result_missing.net_margin_percentage is None

    # Test with zero previous net income
    statements_zero_previous = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            net_income=200000.0,
            operating_income=300000.0,
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            net_income=0.0,
            operating_income=250000.0,
            total_revenue=800000.0,
        ),
    ]

    result_zero_previous = service.calculate_profitability_analysis(statements_zero_previous)

    from datetime import datetime
from backend.repositories.financial_data import FinancialStatement
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

def test_calculate_revenue_analysis():
    service = ResearchService(MockMarketDataProvider())
    statements = [
        FinancialStatement(period=datetime(2025, 3, 31), total_revenue=1000000.0),
        FinancialStatement(period=datetime(2024, 3, 31), total_revenue=800000.0),
    ]
    result = service.calculate_revenue_analysis(statements)

    assert result.current_revenue == 1000000.0
    assert result.previous_revenue == 800000.0
    assert result.growth_percentage == 25.0  # ((1000000 - 800000) / 800000) * 100  

def test_revenue_analysis_with_insufficient_statements():
    service = ResearchService(MockMarketDataProvider())

    statements = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            total_revenue=1000000.0,
        )
    ]

    result = service.calculate_revenue_analysis(statements)

    assert result.growth_percentage is None


def test_revenue_analysis_with_zero_previous_revenue():
    service = ResearchService(MockMarketDataProvider())

    statements = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            total_revenue=0.0,
        ),
    ]

    result = service.calculate_revenue_analysis(statements)

    assert result.current_revenue == 1000000.0
    assert result.previous_revenue == 0.0
    assert result.growth_percentage is None


def test_revenue_analysis_with_missing_revenue():
    service = ResearchService(MockMarketDataProvider())

    statements = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            total_revenue=None,
        ),
    ]

    result = service.calculate_revenue_analysis(statements)

    assert result.growth_percentage is None

# add a method to test calculate_profitability_analysis with various scenarios, including missing data, zero previous net income, and valid data.
def test_calculate_profitability_analysis_with_various_scenarios():
    service = ResearchService(MockMarketDataProvider())

    # Test with valid data
    statements_valid = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            net_income=200000.0,
            operating_income=300000.0,
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            net_income=150000.0,
            operating_income=250000.0,
            total_revenue=800000.0,
        ),
    ]

    result_valid = service.calculate_profitability_analysis(statements_valid)

    assert result_valid.net_profit == 200000.0
    assert result_valid.profit_growth_percentage == 33.33333333333333  # ((200000 - 150000) / 150000) * 100
    assert result_valid.operating_margin_percentage == 30.0  # (300000 / 1000000) * 100
    assert result_valid.net_margin_percentage == 20.0  # (200000 / 1000000) * 100

    # Test with missing data
    statements_missing = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            net_income=None,
            operating_income=None,
            total_revenue=None,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            net_income=None,
            operating_income=None,
            total_revenue=None,
        ),
    ]

    result_missing = service.calculate_profitability_analysis(statements_missing)

    assert result_missing.net_profit is None
    assert result_missing.profit_growth_percentage is None
    assert result_missing.operating_margin_percentage is None
    assert result_missing.net_margin_percentage is None

    # Test with zero previous net income
    statements_zero_previous = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            net_income=200000.0,
            operating_income=300000.0,
            total_revenue=1000000.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            net_income=0.0,
            operating_income=250000.0,
            total_revenue=800000.0,
        ),
    ]

    result_zero_previous = service.calculate_profitability_analysis(statements_zero_previous)

    #add test for eps analysis with various scenarios, including missing data, zero previous eps, and valid data.

def test_calculate_earnings_analysis_with_various_scenarios():
    service = ResearchService(MockMarketDataProvider())

    # Test with valid data
    statements_valid = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            basic_eps=5.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            basic_eps=4.0,
        ),
    ]

    result_valid = service.calculate_earnings_analysis(statements_valid)

    assert result_valid.current_eps == 5.0
    assert result_valid.previous_eps == 4.0
    assert result_valid.eps_growth_percentage == 25.0  # ((5 - 4) / 4) * 100

    # Test with missing data
    statements_missing = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            basic_eps=None,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            basic_eps=None,
        ),
    ]

    result_missing = service.calculate_earnings_analysis(statements_missing)

    assert result_missing.current_eps is None
    assert result_missing.previous_eps is None
    assert result_missing.eps_growth_percentage is None

    # Test with zero previous eps
    statements_zero_previous = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            basic_eps=5.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            basic_eps=0.0,
        ),
    ]

    result_zero_previous = service.calculate_earnings_analysis(statements_zero_previous)

    assert result_zero_previous.current_eps == 5.0
    assert result_zero_previous.previous_eps == 0.0
    assert result_zero_previous.eps_growth_percentage is None

   
    #add test for eps analysis with various scenarios, including missing data, zero previous eps, and valid data.

def test_calculate_earnings_analysis_with_various_scenarios():
    service = ResearchService(MockMarketDataProvider())

    # Test with valid data
    statements_valid = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            basic_eps=5.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            basic_eps=4.0,
        ),
    ]

    result_valid = service.calculate_earnings_analysis(statements_valid)

    assert result_valid.current_eps == 5.0
    assert result_valid.previous_eps == 4.0
    assert result_valid.eps_growth_percentage == 25.0  # ((5 - 4) / 4) * 100

    # Test with missing data
    statements_missing = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            basic_eps=None,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            basic_eps=None,
        ),
    ]

    result_missing = service.calculate_earnings_analysis(statements_missing)

    assert result_missing.current_eps is None
    assert result_missing.previous_eps is None
    assert result_missing.eps_growth_percentage is None

    # Test with zero previous eps
    statements_zero_previous = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            basic_eps=5.0,
        ),
        FinancialStatement(
            period=datetime(2024, 3, 31),
            basic_eps=0.0,
        ),
    ]

    result_zero_previous = service.calculate_earnings_analysis(statements_zero_previous)

    assert result_zero_previous.current_eps == 5.0
    assert result_zero_previous.previous_eps == 0.0
    assert result_zero_previous.eps_growth_percentage is None

def test_earnings_analysis_with_insufficient_statements():
    service = ResearchService(MockMarketDataProvider())

    statements = [
        FinancialStatement(
            period=datetime(2025, 3, 31),
            basic_eps=5.0,
        )
    ]

    result = service.calculate_earnings_analysis(statements)

    assert result.current_eps is None
    assert result.previous_eps is None
    assert result.eps_growth_percentage is None


from backend.models.financial_research import FinancialResearchResult


class MockFinancialDataProvider(MockMarketDataProvider):
    def get_financial_statements(self, symbol: str) -> list[FinancialStatement]:
        return [
            FinancialStatement(
                period=datetime(2025, 3, 31),
                total_revenue=1300.0,
                net_income=105.0,
                operating_income=150.0,
                basic_eps=12.0,
            ),
            FinancialStatement(
                period=datetime(2024, 3, 31),
                total_revenue=1000.0,
                net_income=100.0,
                operating_income=120.0,
                basic_eps=11.0,
            ),
        ]


def test_get_financial_research_result():
    service = ResearchService(MockFinancialDataProvider())

    result = service.get_financial_research_result("RELIANCE.NS")

    assert isinstance(result, FinancialResearchResult)
    assert result.symbol == "RELIANCE.NS"

    assert result.revenue.growth_percentage == 30.0

    assert result.profitability.net_profit == 105.0
    assert result.profitability.profit_growth_percentage == 5.0
    assert result.profitability.operating_margin_percentage == pytest.approx(11.53846, rel=1e-5)
    assert result.profitability.net_margin_percentage == pytest.approx(8.07692, rel=1e-5)

    assert result.earnings.current_eps == 12.0
    assert result.earnings.previous_eps == 11.0
    assert result.earnings.eps_growth_percentage == pytest.approx(9.090909, rel=1e-5)


   