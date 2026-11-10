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

        STRICT RULES:
        1. Do not generate or modify the stock symbol.
        2. The application will populate the symbol.
        3. Only use financial metrics explicitly supplied.
        4. Do not infer market share, demand, expansion or other unsupported facts.
        5. Describe observations as facts only when directly supported by the supplied figures.
        6. Present possible explanations as hypotheses requiring investigation.
        7. Include a concise summary.
        8. Return at least one strength and one risk only when supported by the data.

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
        result["symbol"] = financial_result.symbol  # Ensure the symbol is set correctly    

        return AIResearchResponse.model_validate(result)