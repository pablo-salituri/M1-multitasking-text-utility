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
        return self.provider.query(question)