import os
from dotenv import load_dotenv
from app.core.enums import MODEL_ALIASES

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")            
# ToDo: Realmente hay que definirlo en env? no es mas comodo en codigo?
# ToDo: Ver si se llega a manejar con CLI
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")  
MODEL_PROFILE = os.getenv("MODEL_PROFILE", "cheap")

MODEL_NAME = MODEL_ALIASES.get(
    MODEL_PROFILE,
    MODEL_ALIASES["cheap"]
)

OPENAI_TEMPERATURE = float(
    os.getenv("OPENAI_TEMPERATURE", "0.2")
)

MAX_COMPLETION_TOKENS = int(
    os.getenv("MAX_COMPLETION_TOKENS", "200")
)