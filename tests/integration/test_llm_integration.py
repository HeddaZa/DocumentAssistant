import pytest

from llm.llm_factory import LLMFactory
from structure.llm_call_structure import DocumentType
from structure.state import State


@pytest.fixture
def config() -> dict:
    """Test configuration fixture."""
    return {
        "llm": {
            "type": "ollama",
            "model": "gemma:7b",
        },
    }


@pytest.mark.integration
def test_full_llm_pipeline(config: dict) -> None:
    """Test the complete LLM pipeline from factory creation to response."""
    llm = LLMFactory.create_llm(config)

    test_state = State(
        prompt="Categorize this document. Return type and content.",
        text="This is a medical receipt for 100 EUR from Dr. Smith.",
        result=None,
    )

    result = llm.call(test_state)

    assert isinstance(result, DocumentType)
    assert hasattr(result, "type")
    assert hasattr(result, "price")
    assert hasattr(result, "description")

    assert result.type is not None
    assert isinstance(result.price, (int, float))
    assert isinstance(result.description, str)


@pytest.mark.integration
def test_llm_error_handling(config: dict) -> None:
    """Test error handling with invalid input."""
    llm = LLMFactory.create_llm(config)

    empty_state = State(prompt="Categorize this.", text="", result=None)

    result = llm.call(empty_state)
    assert result is not None


@pytest.mark.integration
def test_long_input_handling(config: dict) -> None:
    """Test handling of longer input texts."""
    llm = LLMFactory.create_llm(config)

    long_text = " ".join(["This is a test document."] * 50)
    test_state = State(prompt="Summarize this text.", text=long_text, result=None)

    result = llm.call(test_state)
    assert result is not None
