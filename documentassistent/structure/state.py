from pydantic import BaseModel

from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
)
from documentassistent.structure.pydantic_llm_calls.invoice_call import (
    InvoiceExtraction,
)
from documentassistent.structure.pydantic_llm_calls.note_call import NoteExtraction
from documentassistent.structure.pydantic_llm_calls.result_call import (
    ResultExtraction,
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
    file_path: str | None = None
    document_id: int | None = None
    invoice_extraction_result: InvoiceExtraction | None = None
    note_extraction_result: NoteExtraction | None = None
    result_extraction_result: ResultExtraction | None = None
