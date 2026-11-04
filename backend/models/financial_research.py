from pydantic import BaseModel

class RevenueAnalysis(BaseModel):
   current_revenue: float | None = None
   previous_revenue: float | None = None
   growth_percentage: float | None = None

class ProfitabilityAnalysis(BaseModel):
   net_profit: float | None = None
   profit_growth_percentage: float | None = None
   operating_margin_percentage: float | None = None
   net_margin_percentage: float | None = None

class EarningsAnalysis(BaseModel):
   current_eps: float | None = None
   previous_eps: float | None = None
   eps_growth_percentage: float | None = None

class FinancialResearchResult(BaseModel):
   symbol: str
   revenue: RevenueAnalysis | None = None
   profitability: ProfitabilityAnalysis | None = None
   earnings: EarningsAnalysis | None = None

