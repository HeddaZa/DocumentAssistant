from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
    DocumentType,
)
from documentassistent.structure.pydantic_llm_calls.confidence import (
    Confidence,
    ConfidenceLevel,
)

EXPLANATION_VALUE = "High confidence"


def test_classification_model_validation() -> None:
    conf = Confidence(level=ConfidenceLevel.HIGH, explanation=EXPLANATION_VALUE)
    obj = Classification(label=DocumentType.INVOICE, confidence=conf)
    assert obj.label == DocumentType.INVOICE
    assert isinstance(obj.confidence, Confidence)
    assert obj.confidence.level == ConfidenceLevel.HIGH
    assert obj.confidence.explanation == EXPLANATION_VALUE
