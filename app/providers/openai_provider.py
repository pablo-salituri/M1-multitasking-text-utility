import json

from openai import OpenAI
from app.services.prompt_service import load_main_prompt
from app.core.config import (
    OPENAI_API_KEY,
    MODEL_NAME,
    OPENAI_TEMPERATURE,
    MAX_COMPLETION_TOKENS
)

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_openai(question: str) -> dict:
    system_prompt = load_main_prompt()
    
    try:
        response = client.responses.create(
            model=MODEL_NAME,
            temperature=OPENAI_TEMPERATURE,
            max_output_tokens=MAX_COMPLETION_TOKENS,

            input=f"""
            {system_prompt}

            User question:
            {question}
            """
        )

        content = response.output_text

        try:
            parsed = json.loads(content)

        # OpenAI response is a text. Not a valid JSON
        except json.JSONDecodeError:
            parsed = {
                "category": "general_inquiry",
                "priority": "low",
                "answer": "The assistant returned an invalid response format.",
                "confidence": 0.0,
                "actions": [
                    "Please try again later"
                ]
            }

        return parsed

    # OpenAI connection problem
    except Exception:
        return {
            "category": "general_inquiry",
            "priority": "high",
            "answer": "The AI provider is currently unavailable.",
            "confidence": 0.0,
            "actions": [
                "Please try again later"
            ]
        }