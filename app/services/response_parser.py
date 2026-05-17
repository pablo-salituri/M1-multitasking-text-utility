import json
from app.models.llm_response_model import LLMResponse


def parse_llm_response(raw_text: str) -> LLMResponse:
    try :
        parsed_json = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed_json = {
            "category": "general_inquiry",
            "priority": "low",
            "answer": "The assistant returned an invalid response format.",
            "confidence": 0.0,
            "actions": [
                "Please try again later"
            ]
        }
    
    return LLMResponse(**parsed_json)