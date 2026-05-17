from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime, timezone

from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse
from app.providers.openai_provider import ask_openai
from app.services.response_parser import parse_llm_response
from app.core.config import MODEL_NAME

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/query", response_model = QueryResponse)
def query_endpoint(request: QueryRequest):
    raw_llm_response = ask_openai(request.question)
    parsed_response = parse_llm_response(raw_llm_response)
    
    return QueryResponse(
        request_id = str(uuid4()),
        timestamp_utc = datetime.now(timezone.utc).isoformat(),
        provider_name = "openai",
        model_used = MODEL_NAME,
        category = parsed_response.category,
        priority = parsed_response.priority,
        answer = parsed_response.answer,
        confidence = parsed_response.confidence,
        actions = parsed_response.actions
    )