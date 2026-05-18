import json
import time
from datetime import datetime, timezone
from openai import OpenAI

from app.services.prompt_service import load_main_prompt
from app.core.config import OPENAI_API_KEY
from app.core.costs import MODEL_COSTS


class OpenAIProvider:
    def __init__(self, model: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def query(self, question: str) -> dict:
        system_prompt = load_main_prompt()
        start_time = time.perf_counter()

        try:
            response = self.client.responses.create(
                model=self.model,
                input=f"""
                {system_prompt}

                User question:
                {question}
                """
            )

            content = response.output_text
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            parsed = self._safe_parse(content)

            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
            total_tokens = response.usage.total_tokens

            # ---------------------------
            # COST CALCULATION (FIXED)
            # ---------------------------
            cost_table = MODEL_COSTS.get(
                self.model,
                MODEL_COSTS["gpt-4.1-mini"]  # fallback seguro
            )

            estimated_cost_usd = round(
                (prompt_tokens * cost_table["input"]) +
                (completion_tokens * cost_table["output"]),
                6
            )

            return {
                "llm_response": parsed,
                "metrics": {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "model": self.model,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "latency_ms": latency_ms,
                    "estimated_cost_usd": estimated_cost_usd
                }
            }

        except Exception:
            return {
                "llm_response": {
                    "category": "general_inquiry",
                    "priority": "low",
                    "answer": "The AI provider is currently unavailable.",
                    "confidence": 0.0,
                    "actions": ["Please try again later"]
                },
                "metrics": {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "model": self.model,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "latency_ms": 0,
                    "estimated_cost_usd": 0.0
                }
            }

    def _safe_parse(self, content: str):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "category": "general_inquiry",
                "priority": "low",
                "answer": "Invalid response format.",
                "confidence": 0.0,
                "actions": ["Please try again later"]
            }