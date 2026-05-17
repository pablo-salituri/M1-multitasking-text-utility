from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import ValidationError

from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse
from app.core.config import MODEL_PROVIDER, MODEL_NAME
from app.providers.provider_manager import ProviderManager
from app.services.metrics_service import log_metrics

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    provider = ProviderManager(
        provider_name=MODEL_PROVIDER,
        model_name=MODEL_NAME
    )

    result = provider.query(request.question)

    response_dict = result["llm_response"]
    metrics_data = result["metrics"]

    try:
        log_metrics(metrics_data)

        return QueryResponse(
            request_id=str(uuid4()),
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            provider_name=MODEL_PROVIDER,
            model_used=MODEL_NAME,

            category=response_dict["category"],
            priority=response_dict["priority"],
            answer=response_dict["answer"],
            confidence=response_dict["confidence"],
            actions=response_dict["actions"]
        )

    # Response does not match the defined schema
    except ValidationError:
        return QueryResponse(
            request_id=str(uuid4()),
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            provider_name="system",
            model_used="fallback",

            category="general_inquiry",
            priority="low",
            answer="The system could not generate a valid response.",
            confidence=0.0,
            actions=["Please try again later"]
        )