from app.services.safety_service import is_prompt_injection, safe_fallback_response
from app.providers.openai_provider import OpenAIProvider


class ProviderManager:
    def __init__(self, provider_name: str, model_name: str):
        self.provider_name = provider_name
        self.model_name = model_name
        self.provider = self._resolve_provider()

    def _resolve_provider(self):
        if self.provider_name == "openai":
            return OpenAIProvider(model=self.model_name)

        raise ValueError(f"Unsupported provider: {self.provider_name}")

    def query(self, question: str):
        # SAFETY LAYER (before LLM call)
        if is_prompt_injection(question):
            return {
                "llm_response": safe_fallback_response(),
                "metrics": {
                    "timestamp_utc": None,
                    "model": self.model_name,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "latency_ms": 0,
                    "estimated_cost_usd": 0.0
                }
            }

        return self.provider.query(question)