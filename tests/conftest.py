import pytest

from documentassistent.structure.state import State


@pytest.fixture
def sample_state() -> State:
    """Create a sample State object for testing purposes."""
    return State(prompt="test prompt", text="test text")


@pytest.fixture
def mock_config() -> dict[str, str | dict[str, str]]:
    """Provide a mock configuration dictionary for testing purposes."""
    return {
        "llm": {
            "type": "ollama",
            "model": "gemma:7b",
        },
    }
