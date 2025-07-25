from unittest.mock import patch

from documentassistent.agents.classification_agent import ClassificationAgent
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
    DocumentType,
)
from documentassistent.structure.pydantic_llm_calls.confidence import (
    Confidence,
    ConfidenceLevel,
)


def test_classification_agent_basic() -> None:
    agent = ClassificationAgent()
    mock_result = Classification(
        label=DocumentType.INVOICE,
        confidence=Confidence(
            level=ConfidenceLevel.HIGH,
            explanation="High confidence",
        ),
    )
    with patch.object(agent.llm, "call", return_value=mock_result):
        result = agent.classify("Sample text")
    assert isinstance(result, Classification)
    assert result.label == DocumentType.INVOICE
