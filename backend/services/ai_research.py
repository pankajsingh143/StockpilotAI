import json

from backend.models.ai_research import AIResearchResponse
from backend.models.financial_research import FinancialResearchResult
from backend.services.ai_research_prompt_builder import AIResearchPromptBuilder


class AIResearchService:
    def __init__(self, ollama_client):
        self.ollama_client = ollama_client
        self.prompt_builder = AIResearchPromptBuilder()

    def analyze(
        self,
        financial_result: FinancialResearchResult,
    ) -> AIResearchResponse:
        prompt = self.prompt_builder.build_prompt(financial_result)

        response = self.ollama_client.generate(
            prompt=prompt,
            format=AIResearchResponse.model_json_schema(),
            )

        result = json.loads(response)
        result["symbol"] = financial_result.symbol  # Ensure the symbol is set correctly    

        return AIResearchResponse.model_validate(result)