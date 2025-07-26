from documentassistent.agents.invoice_agent import InvoiceAgent
from documentassistent.structure.state import State


def test_invoice_agent_basic() -> None:
    agent = InvoiceAgent()
    state = State(
        prompt="Extract invoice information.",
        text="Invoice for GP. Cost 120£. Date 2023-10-01.",
    )
    result = agent.extract_invoice(state)
    assert result is not None
