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
    classification_prompt: str | None = None
    classification_result: Classification | None = None
    text: str


class LLMCall(BaseModel):
    """Pydantic model for LLM calls."""

    prompt: str
    pydantic_object: type
    result: str | None = None
    state: State | None = None

    def __str__(self) -> str:
        """Return a string representation of the LLMCall instance."""
        return (
            f"LLMCall(prompt={self.prompt}, "
            f"pydantic_object={self.pydantic_object.__name__})"
        )

    def __hash__(self) -> int:
        """Return a hash value for the LLMCall instance."""
        return hash((self.prompt, self.pydantic_object))
