from backend.models.financial_reserch import RevenueAnalysis, EarningsAnalysis
from backend.repositories.financial_data import FinancialStatement

from backend.repositories.market_data import (MarketDataProvider, 
                                              StockMarketData
)
class ResearchService:
    def __init__(self, market_data_provider: MarketDataProvider):
        self.market_data_provider = market_data_provider

    def get_stock_research(self, symbol: str) -> StockMarketData:
        return self.market_data_provider.get_stock_data(symbol)

    def calculate_revenue_analysis(self, statements: list[FinancialStatement]) -> RevenueAnalysis:
        if len(statements) < 2:
            return RevenueAnalysis()
        ordered_statements = sorted(statements, key=lambda x: x.period, reverse=True)
        current = ordered_statements[0]
        previous = ordered_statements[1]
        if(
            current.total_revenue is None
            or previous.total_revenue is None
            or previous.total_revenue == 0
        ):
            return RevenueAnalysis(
                current_revenue=current.total_revenue,
                previous_revenue=previous.total_revenue,
                growth_percentage=None
            )
        growth_percentage = ((current.total_revenue - previous.total_revenue) / previous.total_revenue) * 100
        return RevenueAnalysis(
            current_revenue=current.total_revenue,
            previous_revenue=previous.total_revenue,
            growth_percentage=growth_percentage
        )
