import shutil
import subprocess
import time

import pytest

from graphrag.llm.llm_factory import ConfigDict, LLMFactory
from graphrag.structure.llm_call_structure import DocumentType
from graphrag.structure.state import State

pytestmark = pytest.mark.skipif(
    shutil.which("ollama") is None,
    reason="Ollama is not installed",
)


class OllamaNotInstalledError(RuntimeError):
    def __init__(self) -> None:
        msg = "Ollama is not installed or not found in PATH."
        super().__init__(msg)


@pytest.fixture(scope="session", autouse=True)
def ensure_ollama_model() -> None:
    """Ensure Ollama model is available."""
    ollama_path = shutil.which("ollama")
    if ollama_path is None:
        raise OllamaNotInstalledError
    allowed_models = {"gemma:7b"}
    model = "gemma:7b"
    if model not in allowed_models:
        msg = f"Model '{model}' is not allowed."
        raise ValueError(msg)
    subprocess.run([ollama_path, "pull", model], check=True)
    time.sleep(5)


@pytest.fixture
def config() -> dict[str, dict[str, str]]:
    """Test configuration fixture."""
    return {
        "llm": {
            "type": "ollama",
            "model": "gemma:7b",
        },
    }


@pytest.mark.integration
def test_full_llm_pipeline(config: ConfigDict) -> None:
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
    assert isinstance(result.price, int | float)
    assert isinstance(result.description, str)


@pytest.mark.integration
def test_llm_error_handling(config: ConfigDict) -> None:
    """Test error handling with invalid input."""
    llm = LLMFactory.create_llm(config)

    empty_state = State(prompt="Categorize this.", text="", result=None)

    result = llm.call(empty_state)
    assert result is not None


@pytest.mark.integration
def test_long_input_handling(config: ConfigDict) -> None:
    """Test handling of longer input texts."""
    llm = LLMFactory.create_llm(config)

    long_text = " ".join(["This is a test document."] * 50)
    test_state = State(prompt="Summarize this text.", text=long_text, result=None)

    result = llm.call(test_state)
    assert result is not None
