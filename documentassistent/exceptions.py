"""Custom exception classes for the DocumentAssistant application."""


class DocumentAssistantError(Exception):
    """Base exception for all DocumentAssistant errors."""


# ============================================================================
# Configuration Errors
# ============================================================================


class ConfigurationError(DocumentAssistantError):
    """Configuration validation or loading failed."""


class MissingConfigError(ConfigurationError):
    """Required configuration parameter is missing."""


# ============================================================================
# LLM Errors
# ============================================================================


class LLMError(DocumentAssistantError):
    """Base exception for LLM-related errors."""

    DEFAULT_MSG = "LLM operation failed"
    CUSTOM_MSG = "Custom error message"
    WRAPPED_ERROR_MSG = "Wrapped error"


class UnsupportedProviderError(LLMError):
    """LLM provider not supported or invalid."""

    DEFAULT_MSG = "Unsupported provider"

    def __init__(self, msg: str | None = None) -> None:
        super().__init__(msg or self.DEFAULT_MSG)


class LLMConnectionError(LLMError):
    """Failed to connect to LLM service."""


class LLMResponseError(LLMError):
    """LLM returned invalid or malformed response."""


class LLMTimeoutError(LLMError):
    """LLM request exceeded timeout threshold."""


# ============================================================================
# Validation Errors
# ============================================================================


class ValidationError(DocumentAssistantError):
    """Data validation failed."""


class StateValidationError(ValidationError):
    """Workflow state validation failed."""

    DEFAULT_MSG = "State is invalid"
    CUSTOM_MSG = "Custom error message"


class SchemaValidationError(ValidationError):
    """Pydantic schema validation failed."""


# ============================================================================
# Agent Errors
# ============================================================================


class AgentError(DocumentAssistantError):
    """Base exception for agent-related errors."""


class ClassificationError(AgentError):
    """Document classification failed."""

    DEFAULT_MSG = "Classification failed"

    def __init__(self, msg: str | None = None) -> None:
        super().__init__(msg or self.DEFAULT_MSG)


class ExtractionError(AgentError):
    """Information extraction failed."""


class StorageError(AgentError):
    """Data storage operation failed."""


# ============================================================================
# Database Errors
# ============================================================================


class DatabaseError(DocumentAssistantError):
    """Base exception for database operations."""


class DatabaseConnectionError(DatabaseError):
    """Database connection failed."""


class QueryError(DatabaseError):
    """Database query execution failed."""


class RecordNotFoundError(DatabaseError):
    """Requested database record not found."""


# ============================================================================
# File Handling Errors
# ============================================================================


class FileHandlingError(DocumentAssistantError):
    """Base exception for file operations."""


class ThisFileNotFoundError(FileHandlingError):
    """Required file not found at specified path."""


class FileReadError(FileHandlingError):
    """Failed to read file contents."""


class FileWriteError(FileHandlingError):
    """Failed to write file contents."""


class UnsupportedFileTypeError(FileHandlingError):
    """Unsupported file type for processing."""

    DEFAULT_MSG = "Unsupported file type for processing"

    def __init__(self, msg: str | None = None) -> None:
        super().__init__(msg or self.DEFAULT_MSG)


# ============================================================================
# Prompt Errors
# ============================================================================


class PromptError(DocumentAssistantError):
    """Base exception for prompt-related errors."""


class PromptLoadError(PromptError):
    """Failed to load prompt template."""


class PromptRenderError(PromptError):
    """Failed to render prompt with variables."""
