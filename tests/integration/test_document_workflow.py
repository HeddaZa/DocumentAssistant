from documentassistent.agents.classification_agent import ClassificationAgent
from documentassistent.structure.state import State


def test_document_workflow_scenario() -> None:
    agent = ClassificationAgent()

    text = "Sample document text for workflow."
    state = State(prompt="Classify", text=text)
    result = agent.classify(state.text)
    assert result is not None
