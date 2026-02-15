from unittest.mock import Mock

import pytest
from pydantic import BaseModel
from pytest_mock import MockFixture

from documentassistent.exceptions import LLMError
from documentassistent.llm.chain_llm import ChainLLM
from documentassistent.structure.state import State


class DummyPydantic(BaseModel):
    value: str = "test"


def test_chain_creation() -> None:
    """Test the creation of a chain with a prompt and pydantic object."""
    llm = ChainLLM()
    with pytest.raises(LLMError, match="LLM not initialized"):
        llm.create_chain("test prompt", DummyPydantic)


@pytest.fixture
def mock_llm(mocker: MockFixture) -> ChainLLM:
    """Fixture to create a mock LLM instance."""
    llm = ChainLLM()
    llm.llm = mocker.Mock()
    return llm


def test_call_creates_chain(mock_llm: ChainLLM, mocker: MockFixture) -> None:
    """Test that calling the LLM creates a chain if it doesn't exist."""
    from documentassistent.structure.pydantic_llm_calls.invoice_call import (
        DocumentType,
        InvoiceTypeEnum,
        Logs,
    )

    mock_response = DocumentType(
        type=InvoiceTypeEnum.DOCTOR_RECEIPT,
        price=100.0,
        date="2024-05-23",
        description="Doctor visit",
        notes="Regular checkup",
        logs=[Logs(log="Document processed", date="2024-05-23")],
    )

    # Mock the chain creation and invocation
    mocker.patch.object(mock_llm, "create_chain")
    mock_chain = Mock()
    mock_chain.invoke.return_value = mock_response
    mock_llm.chain = mock_chain
    mocker.patch.object(mock_llm, "_current_pydantic_type", DocumentType)

    state = State(prompt="test prompt", text="test text")
    result = mock_llm.call(state, DocumentType)

    mock_chain.invoke.assert_called_once()
    assert isinstance(result, DocumentType)
    assert result.type == InvoiceTypeEnum.DOCTOR_RECEIPT
    assert result.description == "Doctor visit"
