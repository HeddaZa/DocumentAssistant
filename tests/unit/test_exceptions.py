"""Test suite for custom exceptions module."""

import pytest

from documentassistent.exceptions import (
    AgentError,
    ClassificationError,
    ConfigurationError,
    DatabaseConnectionError,
    DatabaseError,
    DocumentAssistantError,
    ExtractionError,
    FileHandlingError,
    FileReadError,
    FileWriteError,
    LLMConnectionError,
    LLMError,
    LLMResponseError,
    LLMTimeoutError,
    MissingConfigError,
    PromptError,
    PromptLoadError,
    PromptRenderError,
    QueryError,
    RecordNotFoundError,
    SchemaValidationError,
    StateValidationError,
    StorageError,
    ThisFileNotFoundError,
    UnsupportedFileTypeError,
    UnsupportedProviderError,
    ValidationError,
)


def test_exception_hierarchy() -> None:
    """Test that all exceptions inherit from DocumentAssistantError."""
    exceptions = [
        ConfigurationError,
        MissingConfigError,
        LLMError,
        UnsupportedProviderError,
        ValidationError,
        StateValidationError,
        AgentError,
        DatabaseError,
        FileHandlingError,
    ]

    for exc_class in exceptions:
        assert issubclass(exc_class, DocumentAssistantError)


def test_llm_exception_hierarchy() -> None:
    """Test LLM exception inheritance."""
    llm_exceptions = [
        UnsupportedProviderError,
        LLMConnectionError,
        LLMResponseError,
        LLMTimeoutError,
    ]

    for exc_class in llm_exceptions:
        assert issubclass(exc_class, LLMError)
        assert issubclass(exc_class, DocumentAssistantError)


def test_validation_exception_hierarchy() -> None:
    """Test validation exception inheritance."""
    validation_exceptions = [StateValidationError, SchemaValidationError]

    for exc_class in validation_exceptions:
        assert issubclass(exc_class, ValidationError)
        assert issubclass(exc_class, DocumentAssistantError)


def test_agent_exception_hierarchy() -> None:
    """Test agent exception inheritance."""
    agent_exceptions = [ClassificationError, ExtractionError, StorageError]

    for exc_class in agent_exceptions:
        assert issubclass(exc_class, AgentError)
        assert issubclass(exc_class, DocumentAssistantError)


def test_database_exception_hierarchy() -> None:
    """Test database exception inheritance."""
    database_exceptions = [
        DatabaseConnectionError,
        QueryError,
        RecordNotFoundError,
    ]

    for exc_class in database_exceptions:
        assert issubclass(exc_class, DatabaseError)
        assert issubclass(exc_class, DocumentAssistantError)


def test_file_exception_hierarchy() -> None:
    """Test file handling exception inheritance."""
    file_exceptions = [
        ThisFileNotFoundError,
        FileReadError,
        FileWriteError,
        UnsupportedFileTypeError,
    ]

    for exc_class in file_exceptions:
        assert issubclass(exc_class, FileHandlingError)
        assert issubclass(exc_class, DocumentAssistantError)


def test_prompt_exception_hierarchy() -> None:
    """Test prompt exception inheritance."""
    prompt_exceptions = [PromptLoadError, PromptRenderError]

    for exc_class in prompt_exceptions:
        assert issubclass(exc_class, PromptError)
        assert issubclass(exc_class, DocumentAssistantError)


def test_exception_messages() -> None:
    """Test that exceptions can be raised with custom messages."""
    with pytest.raises(LLMError, match=LLMError.CUSTOM_MSG):
        raise LLMError(LLMError.CUSTOM_MSG)

    with pytest.raises(StateValidationError, match=StateValidationError.CUSTOM_MSG):
        raise StateValidationError(StateValidationError.DEFAULT_MSG)


def test_catch_base_exception() -> None:
    """Test catching base DocumentAssistantError catches all custom exceptions."""
    exceptions_to_test = [
        MissingConfigError("Config error"),
        UnsupportedProviderError(UnsupportedProviderError.DEFAULT_MSG),
        StateValidationError("Validation error"),
        DatabaseError("DB error"),
        FileReadError("File error"),
    ]

    for exc in exceptions_to_test:
        with pytest.raises(DocumentAssistantError):
            raise exc


def test_catch_category_exception() -> None:
    """Test catching category exceptions works."""
    # LLM category
    with pytest.raises(LLMError):
        raise UnsupportedProviderError(UnsupportedProviderError.DEFAULT_MSG)

    # Validation category
    with pytest.raises(ValidationError):
        raise StateValidationError(StateValidationError.DEFAULT_MSG)

    # Agent category
    with pytest.raises(AgentError):
        raise ClassificationError(ClassificationError.DEFAULT_MSG)


def test_exception_chaining() -> None:
    """Test exception chaining with 'from' clause."""

    def _raise_value_error() -> None:
        """Helper function to raise ValueError."""
        msg = "Original error"
        raise ValueError(msg)

    def _raise_chained_error() -> None:
        """Helper function to raise chained exception."""
        try:
            _raise_value_error()
        except ValueError as e:
            raise LLMError(LLMError.WRAPPED_ERROR_MSG) from e

    with pytest.raises(LLMError) as exc_info:
        _raise_chained_error()

    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "Original error"
