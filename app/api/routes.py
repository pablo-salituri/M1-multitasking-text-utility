from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime, timezone

from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse
from app.core.enums import CategoryEnum, PriorityEnum
from app.providers.openai_provider import ask_openai

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/query", response_model = QueryResponse)
def query_endpoint(request: QueryRequest):
    return QueryResponse(
        request_id = str(uuid4()),
        timestamp_utc = datetime.now(timezone.utc).isoformat(),
        provider_name = "dummy",
        model_used = "dummy",
        category = CategoryEnum.GENERAL_INQUIRY,
        priority = PriorityEnum.LOW,
        answer = ask_openai(request.question),
        confidence = 0.0,
        actions = []
    )