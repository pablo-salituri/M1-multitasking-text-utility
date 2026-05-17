from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    MODEL_NAME,
    OPENAI_TEMPERATURE,
    MAX_COMPLETION_TOKENS
)

client = OpenAI(api_key = OPENAI_API_KEY)


def ask_openai(question: str) -> str:
    response = client.responses.create(
        model = MODEL_NAME,
        temperature = OPENAI_TEMPERATURE,
        max_output_tokens = MAX_COMPLETION_TOKENS,
        
        input = f"""
            Answer the following customer support question briefly.input
            
            User question:
            {question}
        """
    )
    
    return response.output_text