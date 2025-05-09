import pytest

from llm.llm_factory import LLMFactory
from llm.ollama_llm import OllamaLLMCall


def test_create_llm_with_ollama() -> None:
    """Test creating an LLM with the Ollama type."""
    config = {
        "llm": {
            "type": "ollama",
            "model": "gemma:7b",
        },
    }
    llm = LLMFactory.create_llm(config)
    assert isinstance(llm, OllamaLLMCall)


def test_create_llm_with_invalid_type() -> None:
    """Test creating an LLM with an invalid type."""
    config = {
        "llm": {
            "type": "invalid",
        },
    }
    with pytest.raises(ValueError, match="Invalid LLM type: invalid"):
        LLMFactory.create_llm(config)
