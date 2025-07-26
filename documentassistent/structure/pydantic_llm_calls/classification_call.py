from enum import Enum

from pydantic import BaseModel, Field, field_validator

from documentassistent.structure.pydantic_llm_calls.confidence import Confidence


class DocumentType(str, Enum):
    """Enumeration for different types of documents."""

    INVOICE = "invoice"
    RESULT = "result"
    NOTE = "note"


class Classification(BaseModel):
    """Represents a classification result with a label and confidence score."""

    label: DocumentType = Field(
        description=(
            "The type of document classified, such as invoice, result, or note."
        ),
    )
    confidence: Confidence = Field(
        description=("The confidence level of the result, including an explanation."),
    )

    @field_validator("label", mode="before")
    @classmethod
    def normalize_label(cls, v: str) -> str:
        """Normalize the label to lowercase and strip whitespace."""
        return v.strip().lower() if isinstance(v, str) else v
