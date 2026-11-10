from pydantic import BaseModel

class AIResearchResponse(BaseModel):
    symbol: str
    summary: str | None = None
    strengths: list[str] | None = None
    risks: list[str] | None = None  