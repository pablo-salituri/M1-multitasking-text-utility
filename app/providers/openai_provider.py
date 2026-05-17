import json
import time

from datetime import datetime, timezone
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
    start_time = time.perf_counter()
    
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
        
        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )
        
        prompt_tokens = response.usage.input_tokens
        completion_tokens = response.usage.output_tokens
        total_tokens = response.usage.total_tokens
        
        estimated_cost_usd = round(
            (
                (prompt_tokens * 0.0000004) +
                (completion_tokens * 0.0000016)
            ),
            6
        )

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

        return {
            "llm_response": parsed,
            "metrics": {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "model": MODEL_NAME,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "latency_ms": latency_ms,
                "estimated_cost_usd": estimated_cost_usd
            }
        }


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