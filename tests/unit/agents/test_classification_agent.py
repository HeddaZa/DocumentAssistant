from unittest.mock import patch

from documentassistent.agents.classification_agent import ClassificationAgent
from documentassistent.prompts.prompt_collection import CATEGORISATION_PROMPT
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
    DocumentType,
)
from documentassistent.structure.pydantic_llm_calls.confidence import (
    Confidence,
    ConfidenceLevel,
)
from documentassistent.structure.state import State


def test_classification_agent_basic() -> None:
    agent = ClassificationAgent()
    mock_result = Classification(
        label=DocumentType.INVOICE,
        confidence=Confidence(
            level=ConfidenceLevel.HIGH,
            explanation="High confidence",
        ),
    )
    state = State(
        prompt=CATEGORISATION_PROMPT,
        text="Invoice for treatment on the 2.4.21 by Dr. Smith.",
    )
    with patch.object(agent.llm, "call", return_value=mock_result):
        result = agent.classify(state)
    assert isinstance(result, State)
    assert isinstance(result.classification_result, Classification)
    assert result.classification_result.label == DocumentType.INVOICE
