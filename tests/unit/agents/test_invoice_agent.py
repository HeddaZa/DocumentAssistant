from documentassistent.agents.invoice_agent import InvoiceAgent


def test_invoice_agent_basic() -> None:
    agent = InvoiceAgent()
    text = "Invoice for GP. Cost 120£. Date 2023-10-01."
    result = agent.extract_invoice(text)
    assert result is not None
