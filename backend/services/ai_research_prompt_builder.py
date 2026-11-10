from textwrap import dedent

from backend.models.financial_research import FinancialResearchResult


class AIResearchPromptBuilder:
    def build_prompt(self, financial_result: FinancialResearchResult) -> str:
        revenue = (
            financial_result.revenue.model_dump_json()
            if financial_result.revenue
            else "Not available"
        )
        profitability = (
            financial_result.profitability.model_dump_json()
            if financial_result.profitability
            else "Not available"
        )
        earnings = (
            financial_result.earnings.model_dump_json()
            if financial_result.earnings
            else "Not available"
        )

        return dedent(
            f"""
            You are a financial research analyst.

            Interpret only the verified financial metrics supplied below.

            Stock: {financial_result.symbol}

            Revenue analysis:
            {revenue}

            Profitability analysis:
            {profitability}

            Earnings analysis:
            {earnings}

            Instructions:

            1. Identify meaningful financial strengths and risks supported by the data.
            2. Compare revenue growth with net profit growth when both are available.
            3. Compare EPS growth with revenue growth and net profit growth when available.
            4. Identify meaningful differences between these growth rates.
            5. Explicitly mention when important metrics are unavailable.
            6. Provide a concise summary.
            7. Do not provide buy or sell recommendations.

            Strict rules:

            1. Do not generate or modify the stock symbol.
            2. Use only the financial metrics explicitly supplied.
            3. Do not infer market share, demand, expansion, cash flow, debt or other unsupported facts.
            4. Do not attribute financial performance to specific business causes without supporting evidence.
            5. When growth rates differ, describe the divergence without assuming its cause.
            6. Distinguish verified observations from possible explanations.
            7. Present possible explanations only as hypotheses requiring further investigation.
            8. Do not describe revenue growth alone as proof of strong financial health.
            9. Do not invent strengths or risks when the data does not support them.

            Return only valid JSON in this exact structure:

            {{
                "symbol": "{financial_result.symbol}",
                "summary": "A concise financial interpretation",
                "strengths": ["strength 1"],
                "risks": ["risk 1"]
            }}
            """
        ).strip()
