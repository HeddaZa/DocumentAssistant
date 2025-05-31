from abc import ABC, abstractmethod

from documentassistent.structure.pydantic_llm_calls.invoice_call import DocumentType
from documentassistent.structure.state import State
from documentassistent.utils.logger import setup_logger

logger = setup_logger(name="BaseLLM", log_file="logs/base_llm.log")


class BaseLLM(ABC):
    """Abstract base class for LLMs."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model

        logger.info("%s initialized.", self.__class__.__name__)

    @abstractmethod
    def call(self, state: State, pydantic_object: type) -> DocumentType:
        """Abstract method to call the LLM with a prompt."""
        logger.debug("call() method invoked with state: %s", state)
        error_message = "Subclasses must implement call method"
        raise NotImplementedError(error_message)
