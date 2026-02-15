import shutil
from unittest.mock import Mock

import pytest

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

pytestmark = pytest.mark.skipif(
    shutil.which("ollama") is None,
    reason="Ollama is not installed",
)


def test_invoice_agent_basic() -> None:
    mock_llm = Mock()
    agent = InvoiceAgent(llm=mock_llm)

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

    from documentassistent.structure.pydantic_llm_calls.invoice_call import (
        DocumentType as InvoiceDocType,
    )
    from documentassistent.structure.pydantic_llm_calls.invoice_call import (
        InvoiceTypeEnum,
        Logs,
    )

    mock_response = InvoiceDocType(
        type=InvoiceTypeEnum.DOCTOR_RECEIPT,
        price=120.0,
        date="2023-10-01",
        description="GP visit",
        notes="Test invoice",
        logs=[Logs(log="Extracted", date="2023-10-01")],
    )
    mock_llm.call.return_value = mock_response

    result = agent.extract_invoice(state)
    assert result is not None
    assert mock_llm.call.called
