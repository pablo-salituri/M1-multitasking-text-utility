import re


BLOCK_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"you are now",
    r"act as",
    r"forget everything",
]


def is_prompt_injection(text: str) -> bool:
    text_lower = text.lower()

    if len(text_lower.strip()) < 3:
        return True

    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    return False


def safe_fallback_response():
    return {
        "category": "general_inquiry",
        "priority": "low",
        "answer": "I cannot process this request as it is unclear or potentially unsafe.",
        "confidence": 0.0,
        "actions": [
            "Rephrase your question clearly",
            "Avoid including system or instruction-like text"
        ]
    }