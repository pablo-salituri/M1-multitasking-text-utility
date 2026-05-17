from pydantic import BaseModel, Field

from app.core.enums import CategoryEnum, PriorityEnum

class LLMResponse(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    answer: str
    confidence: float = Field(
        ge = 0.0,
        le =1.0
    )
    actions: list[str] = Field(
        min_length = 1
    )