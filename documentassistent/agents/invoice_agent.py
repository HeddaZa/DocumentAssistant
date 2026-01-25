from documentassistent.agents.base_agent import BaseAgent, validate_state
from documentassistent.llm.base_llm import BaseLLM
from documentassistent.structure.pydantic_llm_calls.invoice_call import (
    InvoiceExtraction,
)
from documentassistent.structure.state import BaseWorkflowState, InvoiceExtractionState
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="InvoiceAgent",
    log_file="logs/invoice_agent.log",
)


class InvoiceAgent(BaseAgent):
    """
    Agent for recognizing and extracting information from invoices using LLMFactory.

    This agent uses a factory to instantiate the LLM, a custom prompt, and a
    Pydantic structure for invoice extraction tasks.
    """

    def __init__(self, llm: BaseLLM | None = None) -> None:
        super().__init__(agent_name="InvoiceAgent", logger=logger, llm=llm)

    @validate_state
    def extract_invoice(self, state: BaseWorkflowState) -> InvoiceExtractionState:
        """Extract invoice information from the input text."""
        state = self._convert_state(state, InvoiceExtractionState)
        result = self.llm.call(state, pydantic_object=InvoiceExtraction)
        logger.debug("Invoice extraction result: {}", result)
        return state.model_copy(update={"invoice_extraction_result": result})
