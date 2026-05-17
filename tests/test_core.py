from app.services.response_parser import parse_llm_response


def test_parse_valid_json_response():
    raw_response = """
    {
        "category": "billing",
        "priority": "high",
        "answer": "Duplicate charge detected.",
        "confidence": 0.91,
        "actions": [
            "Review billing history"
        ]
    }
    """

    parsed = parse_llm_response(raw_response)

    assert parsed.category == "billing"
    assert parsed.priority == "high"
    assert parsed.answer == "Duplicate charge detected."
    assert parsed.confidence == 0.91
    assert parsed.actions == ["Review billing history"]
    
    
    
def test_parse_invalid_json_response():
    raw_response = "invalid json"
    
    parsed = parse_llm_response(raw_response)
    
    assert parsed.category == "general_inquiry"
    assert parsed.priority == "low"
    assert parsed.confidence == 0.0