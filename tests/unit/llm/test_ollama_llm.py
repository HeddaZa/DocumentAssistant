from unittest.mock import Mock

import pytest

from documentassistent.llm.ollama_llm import OllamaLLMCall
from documentassistent.structure.state import State


@pytest.fixture
def mock_ollama_llm(mocker: Mock) -> OllamaLLMCall:
    """Fixture to create a mocked OllamaLLM instance."""
    mocker.patch("documentassistent.llm.ollama_llm.OllamaLLM")
    return OllamaLLMCall(model="gemma:7b")


@pytest.fixture
def sample_state() -> State:
    """Fixture to create a sample state."""
    return State(prompt="Test prompt", text="This is a test document", result=None)


def test_ollama_llm_initialization() -> None:
    """Test OllamaLLM initialization with default model."""
    llm = OllamaLLMCall()
    assert llm.llm is not None
    assert llm.chain is None


def test_ollama_llm_initialization_with_custom_model() -> None:
    """Test OllamaLLM initialization with custom model."""
    model_name = "gemma:7b"
    llm = OllamaLLMCall(model=model_name)
    assert llm.llm is not None


def test_ollama_llm_call(mock_ollama_llm: OllamaLLMCall, sample_state: State) -> None:
    """Test OllamaLLM call method."""
    from documentassistent.structure.pydantic_llm_calls.invoice_call import (
        DocumentType,
        InvoiceTypeEnum,
        Logs,
    )

    mock_ollama_llm.chain = Mock()
    mock_response = DocumentType(
        type=InvoiceTypeEnum.DOCTOR_RECEIPT,
        price=100.0,
        date="2024-05-24",
        description="Test description",
        notes="Test notes",
        logs=[Logs(log="Test log", date="2024-05-24")],
    )
    mock_ollama_llm.chain.invoke.return_value = mock_response

    result = mock_ollama_llm.call(sample_state, DocumentType)

    mock_ollama_llm.chain.invoke.assert_called_once_with(
        {"text": sample_state.text},
        return_only_outputs=True,
    )
    assert isinstance(result, DocumentType)
    assert result.type == InvoiceTypeEnum.DOCTOR_RECEIPT
    assert result.description == "Test description"


def test_ollama_llm_chain_creation(mock_ollama_llm: OllamaLLMCall) -> None:
    """Test chain creation in OllamaLLM."""
    from documentassistent.structure.pydantic_llm_calls.invoice_call import DocumentType

    prompt = "Test prompt"
    mock_ollama_llm.create_chain(prompt, DocumentType)
    assert mock_ollama_llm.chain is not None


def test_ollama_llm_error_handling(mocker: Mock) -> None:
    """Test error handling when Ollama service is not available."""
    mocker.patch(
        "documentassistent.llm.ollama_llm.OllamaLLM",
        side_effect=ConnectionError,
    )

    with pytest.raises(ConnectionError):
        OllamaLLMCall(model="gemma:7b")
