import pytest

from structure.state import State


@pytest.fixture
def sample_state() -> State:
    """Create a sample State object for testing purposes."""
    return State(prompt="test prompt", text="test text", result=None)


@pytest.fixture
def mock_config() -> dict:
    """Provide a mock configuration dictionary for testing purposes."""
    return {
        "llm": {
            "type": "ollama",
            "model": "gemma:7b",
        },
    }
