from pydantic import BaseModel

from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
)


class Document(BaseModel):
    """Represents a document with content and optional metadata."""

    content: str
    metadata: dict | None = {}


class State(BaseModel):
    """Pydantic model for representing the state."""

    prompt: str
    result: str | None = None
    document: Document | None = None
    classification_result: Classification | None = None
    special_agent_result: str | None = None
    text: str
