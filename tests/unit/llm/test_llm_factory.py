import pytest

from documentassistent.llm.llm_factory import ConfigDict, LLMConfig, LLMFactory
from documentassistent.llm.ollama_llm import OllamaLLMCall


def test_create_llm_with_ollama() -> None:
    """Test creating an LLM with the Ollama type."""
    config: ConfigDict = {"llm": LLMConfig(type="ollama", model="gemma:7b")}
    llm = LLMFactory.create_llm(config)
    assert isinstance(llm, OllamaLLMCall)


def test_create_llm_with_invalid_type() -> None:
    """Test creating an LLM with an invalid type."""
    config: ConfigDict = {"llm": LLMConfig(type="invalid", model=None)}
    with pytest.raises(ValueError, match="Unsupported LLM type: 'invalid'"):
        LLMFactory.create_llm(config)
