import json

from backend.models.ai_research import AIResearchResponse
from backend.models.financial_research import FinancialResearchResult


class AIResearchService:
    def __init__(self, ollama_client):
        self.ollama_client = ollama_client

    def analyze(
        self,
        financial_result: FinancialResearchResult,
    ) -> AIResearchResponse:

        prompt = f"""
        You are a financial research analyst.

        Interpret the following verified financial metrics.

        Stock: {financial_result.symbol}

        Revenue analysis:
        {financial_result.revenue.model_dump_json() if financial_result.revenue else "Not available"}

        Instructions:
        1. Identify meaningful financial strengths.
        2. Identify potential financial risks.
        3. Do not invent missing financial information.
        4. Distinguish facts from possible explanations.
        5. Do not provide buy or sell recommendations.

        Return only valid JSON in this exact structure:
        {{
            "symbol": "{financial_result.symbol}",
            "summary": "A concise financial interpretation",
            "strengths": ["strength 1"],
            "risks": ["risk 1"]
        }}
        """

        response = self.ollama_client.generate(
            prompt=prompt,
            format = AIResearchResponse.model_json_schema(),
            )

        result = json.loads(response)

        return AIResearchResponse.model_validate(result)