from backend.models.financial_research import RevenueAnalysis, EarningsAnalysis, ProfitabilityAnalysis, FinancialResearchResult
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
    
    def calculate_profitability_analysis(
        self,
        statements: list[FinancialStatement],
    ) -> ProfitabilityAnalysis:

        if len(statements) < 2:
            return ProfitabilityAnalysis()

        ordered_statements = sorted(
            statements,
            key=lambda x: x.period,
            reverse=True,
        )

        current = ordered_statements[0]
        previous = ordered_statements[1]

        profit_growth = None

        if (
            current.net_income is not None
            and previous.net_income is not None
            and previous.net_income > 0
        ):
            profit_growth = (
                (current.net_income - previous.net_income)
                / abs(previous.net_income)
            ) * 100

        operating_margin = None

        if (
            current.operating_income is not None
            and current.total_revenue is not None
            and current.total_revenue != 0
        ):
            operating_margin = (
                current.operating_income / current.total_revenue
            ) * 100

        net_margin = None

        if (
            current.net_income is not None
            and current.total_revenue is not None
            and current.total_revenue != 0
        ):
            net_margin = (
                current.net_income / current.total_revenue
            ) * 100

        return ProfitabilityAnalysis(
            net_profit=current.net_income,
            profit_growth_percentage=profit_growth,
            operating_margin_percentage=operating_margin,
            net_margin_percentage=net_margin,
        )
    
    def calculate_earnings_analysis(
        self,
        statements: list[FinancialStatement],
    ) -> EarningsAnalysis:

        if len(statements) < 2:
            return EarningsAnalysis()

        ordered_statements = sorted(
            statements,
            key=lambda x: x.period,
            reverse=True,
        )

        current = ordered_statements[0]
        previous = ordered_statements[1]

        eps_growth = None

        if (
            current.basic_eps is not None
            and previous.basic_eps is not None
            and previous.basic_eps > 0
        ):
            eps_growth = (
                (current.basic_eps - previous.basic_eps)
                / previous.basic_eps
            ) * 100

        return EarningsAnalysis(
            current_eps=current.basic_eps,
            previous_eps=previous.basic_eps,
            eps_growth_percentage=eps_growth,
        )

    def get_financial_research_result(
        self,
        symbol: str,
    ) -> FinancialResearchResult:

        statements = self.market_data_provider.get_financial_statements(symbol)

        return FinancialResearchResult(
            symbol=symbol,
            revenue=self.calculate_revenue_analysis(statements),
            profitability=self.calculate_profitability_analysis(statements),
            earnings=self.calculate_earnings_analysis(statements),
        )

            
