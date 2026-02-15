import shutil
import subprocess

import pytest

from documentassistent.agents.classification_agent import ClassificationAgent
from documentassistent.structure.state import State


def is_ollama_running() -> bool:
    """Check if Ollama server is running."""
    try:
        ollama_path = shutil.which("ollama")
        if ollama_path is None:
            return False
        result = subprocess.run(
            [ollama_path, "list"],
            capture_output=True,
            timeout=2,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    else:
        return result.returncode == 0


pytestmark = pytest.mark.skipif(
    not is_ollama_running(),
    reason="Ollama is not running",
)


def test_document_workflow_scenario() -> None:
    agent = ClassificationAgent()

    text = "Sample document text for workflow."
    state = State(prompt="Classify", text=text)
    result = agent.classify(state)
    assert result is not None
