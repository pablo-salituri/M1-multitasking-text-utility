from openai import OpenAI
from app.services.prompt_service import load_main_prompt
from app.core.config import (
    OPENAI_API_KEY,
    MODEL_NAME,
    OPENAI_TEMPERATURE,
    MAX_COMPLETION_TOKENS
)


client = OpenAI(api_key = OPENAI_API_KEY)


def ask_openai(question: str) -> str:
    system_prompt = load_main_prompt()
    
    response = client.responses.create(
        model = MODEL_NAME,
        temperature = OPENAI_TEMPERATURE,
        max_output_tokens = MAX_COMPLETION_TOKENS,
        
        input = f"""
            {system_prompt}
            
            User question:
            {question}
        """
    )
    
    return response.output_text