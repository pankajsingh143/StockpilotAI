from fastapi import APIRouter, Depends

from backend.services.research import ResearchService
from backend.api.dependencies import (
    get_research_service,
    get_ai_research_service,
)
from backend.services.ai_research import AIResearchService
from backend.models.ai_research import AIResearchResponse
research_router = APIRouter(prefix="/stocks", tags=["Research"])

@research_router.get("/{symbol}/research")
def get_stock_research(symbol: str,
                          service: ResearchService = Depends(get_research_service),
                          ):
        return service.get_stock_research(symbol)

@research_router.get(
    "/{symbol}/ai-research",
    response_model=AIResearchResponse,
)
def get_ai_stock_research(
    symbol: str,
    research_service: ResearchService = Depends(get_research_service),
    ai_service: AIResearchService = Depends(get_ai_research_service),
):
    financial_result = research_service.get_financial_research_result(symbol)

    return ai_service.analyze(financial_result)