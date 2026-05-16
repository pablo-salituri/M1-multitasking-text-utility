from pydantic import BaseModel
from typing import List

from app.core.enums import CategoryEnum, PriorityEnum


class QueryResponse(BaseModel):
    request_id: str
    timestamp_utc: str
    provider_name: str
    model_used: str
    category: CategoryEnum
    priority: PriorityEnum
    answer: str
    confidence: float
    actions: List[str]