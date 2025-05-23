from abc import ABC, abstractmethod

from utils.logger import setup_logger

# Set up a logger for the LLM module
logger = setup_logger(name="BaseLLM", log_file="logs/base_llm.log")


class BaseLLM(ABC):
    """Abstract base class for LLMs."""

    def __init__(self):
        logger.info("%s initialized.", self.__class__.__name__)

    @abstractmethod
    def call(self, prompt: str) -> str:
        """Abstract method to call the LLM with a prompt."""
        logger.debug("call() method invoked with prompt: %s", prompt)
