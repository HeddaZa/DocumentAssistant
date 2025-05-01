from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Abstract base class for LLMs."""

    @abstractmethod
    def call(self, prompt: str) -> str:
        """Abstract method to call the LLM with a prompt.

        Args:
            prompt (str): The input prompt.

        Returns:
            str: The response from the LLM.
        """
