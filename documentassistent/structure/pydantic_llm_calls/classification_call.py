from enum import Enum

from pydantic import BaseModel, Field

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
