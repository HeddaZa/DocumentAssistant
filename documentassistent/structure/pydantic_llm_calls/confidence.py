from enum import Enum

from pydantic import BaseModel, Field


class ConfidenceLevel(str, Enum):
    """Enumeration for confidence levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Confidence(BaseModel):
    """Represents the confidence level of a classification result."""

    level: ConfidenceLevel = Field(
        description=(
            "The confidence level of the classification result: high, medium, or low."
        ),
    )
    explanation: str = Field(
        description="Explanation why ConfidenceLevel was chosen.",
    )
