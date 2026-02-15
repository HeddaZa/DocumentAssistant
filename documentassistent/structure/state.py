from pydantic import BaseModel, model_validator

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


# ============================================================================
# Focused State Models - Workflow Stage Pattern
# ============================================================================


class BaseWorkflowState(BaseModel):
    """Base state for all document processing workflows."""

    text: str
    file_path: str | None = None
    document_id: int | None = None


class ClassificationState(BaseWorkflowState):
    """State for document classification stage."""

    prompt: str = ""
    classification_result: Classification | None = None

    @model_validator(mode="after")
    def set_default_prompt(self) -> "ClassificationState":
        """Set default categorization prompt if not provided."""
        if not self.prompt:
            from documentassistent.prompts.prompt_collection import (
                CATEGORISATION_PROMPT,
            )

            self.prompt = CATEGORISATION_PROMPT
        return self


class ExtractionState(BaseWorkflowState):
    """Base state for extraction workflows - requires classification."""

    prompt: str = ""
    classification_result: Classification


class InvoiceExtractionState(ExtractionState):
    """State for invoice extraction workflow."""

    invoice_extraction_result: InvoiceExtraction | None = None

    @model_validator(mode="after")
    def set_default_prompt(self) -> "InvoiceExtractionState":
        """Set default invoice extraction prompt if not provided."""
        if not self.prompt:
            from documentassistent.prompts.prompt_collection import (
                INVOICE_EXTRACTION_PROMPT,
            )

            self.prompt = INVOICE_EXTRACTION_PROMPT
        return self


class NoteExtractionState(ExtractionState):
    """State for note extraction workflow."""

    note_extraction_result: NoteExtraction | None = None

    @model_validator(mode="after")
    def set_default_prompt(self) -> "NoteExtractionState":
        """Set default note extraction prompt if not provided."""
        if not self.prompt:
            from documentassistent.prompts.prompt_collection import (
                NOTE_EXTRACTION_PROMPT,
            )

            self.prompt = NOTE_EXTRACTION_PROMPT
        return self


class ResultExtractionState(ExtractionState):
    """State for medical result extraction workflow."""

    result_extraction_result: ResultExtraction | None = None

    @model_validator(mode="after")
    def set_default_prompt(self) -> "ResultExtractionState":
        """Set default result extraction prompt if not provided."""
        if not self.prompt:
            from documentassistent.prompts.prompt_collection import (
                RESULT_EXTRACTION_PROMPT,
            )

            self.prompt = RESULT_EXTRACTION_PROMPT
        return self


class StorageState(BaseWorkflowState):
    """State after document has been stored."""

    classification_result: Classification
    document_id: int | None = None  # Set during storage
    extraction_result: InvoiceExtraction | NoteExtraction | ResultExtraction | None = (
        None
    )


# ============================================================================
# Type Aliases and Backward Compatibility
# ============================================================================

# Union type for all workflow states
WorkflowState = (
    ClassificationState
    | InvoiceExtractionState
    | NoteExtractionState
    | ResultExtractionState
    | StorageState
)

# Backward compatibility: Legacy State class
# This maintains compatibility with existing code
State = ClassificationState  # Default to most commonly used state
