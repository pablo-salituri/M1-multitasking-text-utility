from enum import Enum


class CategoryEnum(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    ACCOUNT_MANAGEMENT = "account_management"
    SUBSCRIPTION = "subscription"
    GENERAL_INQUIRY = "general_inquiry"


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


MODEL_ALIASES = {
    "cheap": "gpt-4.1-mini",
    "smart": "gpt-4.1"
}