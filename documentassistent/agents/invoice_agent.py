from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.prompts.prompt_collection import INVOICE_EXTRACTION_PROMPT
from documentassistent.structure.pydantic_llm_calls.invoice_call import (
    InvoiceExtraction,
)
from documentassistent.structure.state import LLMCall, State
from documentassistent.utils.logger import setup_logger
from load_config import load_config

logger = setup_logger(
    name="InvoiceAgent",
    log_file="logs/invoice_agent.log",
)
CONFIG = load_config("config.yaml")


class InvoiceAgent:
    """
    Agent for recognizing and extracting information from invoices using LLMFactory.

    This agent uses a factory to instantiate the LLM, a custom prompt, and a
    Pydantic structure for invoice extraction tasks.
    """

    def __init__(self) -> None:
        config: ConfigDict = {
            "llm": {
                "type": "ollama",
                "model": CONFIG["ollama"]["model"],
            },
        }
        self.llm = LLMFactory.create_llm(config)
        logger.info(
            "InvoiceAgent initialized with LLM",
            extra={"llm_type": type(self.llm).__name__},
        )

    def extract_invoice(self, text: str) -> InvoiceExtraction:
        """Extract invoice information from the input text."""
        state = State(
            prompt=INVOICE_EXTRACTION_PROMPT,
            text=text,
            result=None,
        )
        llm_call = LLMCall(
            prompt=INVOICE_EXTRACTION_PROMPT,
            pydantic_object=InvoiceExtraction,
            state=state,
        )
        if llm_call.state is None:
            msg = "LLMCall.state must not be None"
            raise ValueError(msg)
        result = self.llm.call(llm_call.state, pydantic_object=InvoiceExtraction)
        if not isinstance(result, InvoiceExtraction):
            msg = f"Expected InvoiceExtraction, got {type(result)}"
            raise TypeError(msg)
        logger.debug("Invoice extraction result: {}", result)
        return result
