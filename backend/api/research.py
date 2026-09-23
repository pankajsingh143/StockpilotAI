from fastapi import APIRouter, Depends

from backend.api.dependencies import get_research_service
from backend.services.research import ResearchService

research_router = APIRouter(prefix="/stocks", tags=["Research"])

@research_router.get("/{symbol}/research")
def get_stock_research(symbol: str,
                          service: ResearchService = Depends(get_research_service),
                          ):
        return service.get_stock_research(symbol)

   