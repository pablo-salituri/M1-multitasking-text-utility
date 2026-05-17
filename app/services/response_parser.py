import json
from app.models.llm_response_model import LLMResponse


def parse_llm_response(raw_text: str) -> LLMResponse:
    parsed_json = json.loads(raw_text)
    validated_response = LLMResponse(**parsed_json)
    
    return validated_response