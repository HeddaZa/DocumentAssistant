from documentassistent.agents.invoice_agent import InvoiceAgent
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
    DocumentType,
)
from documentassistent.structure.pydantic_llm_calls.confidence import (
    Confidence,
    ConfidenceLevel,
)
from documentassistent.structure.state import InvoiceExtractionState


def test_invoice_agent_basic() -> None:
    agent = InvoiceAgent()

    # Create a mock classification result
    classification = Classification(
        label=DocumentType.INVOICE,
        confidence=Confidence(
            level=ConfidenceLevel.HIGH,
            explanation="High confidence",
        ),
    )

    state = InvoiceExtractionState(
        prompt="Extract invoice information.",
        text="Invoice for GP. Cost 120£. Date 2023-10-01.",
        classification_result=classification,
    )
    result = agent.extract_invoice(state)
    assert result is not None
