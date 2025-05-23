from abc import ABC, abstractmethod

from utils.logger import setup_logger

logger = setup_logger(name="BaseLLM", log_file="logs/base_llm.log")


class BaseLLM(ABC):
    """Abstract base class for LLMs."""

    @abstractmethod
    def __init__(self) -> None:
        logger.info("%s initialized.", self.__class__.__name__)

    @abstractmethod
    def call(self, prompt: str) -> str:
        """Abstract method to call the LLM with a prompt."""
        logger.debug("call() method invoked with prompt: %s", prompt)
        error_message = "Subclasses must implement call method"
        raise NotImplementedError(error_message)
