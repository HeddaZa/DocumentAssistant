import pytest
from pytest_mock import MockFixture

from graphrag.llm.chain_llm import ChainLLM
from graphrag.structure.state import State


def test_chain_creation() -> None:
    """Test the creation of a chain with a prompt."""
    llm = ChainLLM()
    with pytest.raises(ValueError, match="LLM not initialized"):
        llm.create_chain("test prompt")


@pytest.fixture
def mock_llm(mocker: MockFixture) -> None:
    """Fixture to create a mock LLM instance."""
    llm = ChainLLM()
    llm.llm = mocker.Mock()
    return llm


def test_call_creates_chain(mock_llm: ChainLLM) -> None:
    """Test that calling the LLM creates a chain if it doesn't exist."""
    mock_response = """
    {
        "type": "receipt_from_doctor",
        "price": 100.0,
        "date": "2024-05-23",
        "description": "Doctor visit",
        "notes": "Regular checkup",
        "logs": [
            {
                "log": "Document processed",
                "date": "2024-05-23"
            }
        ]
    }
    """
    mock_llm.llm.return_value = mock_response

    state = State(prompt="test prompt", text="test text", result=None)
    mock_llm.call(state)
    assert mock_llm.chain is not None
