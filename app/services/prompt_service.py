from pathlib import Path

PROMPT_PATH = Path("prompts/main_prompt.md")

def load_main_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")