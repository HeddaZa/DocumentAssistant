from llm.base_llm import BaseLLM
from utils.logger import setup_logger

logger = setup_logger(name="OllamaLLM")


class OllamaLLM(BaseLLM):
    """Ollama LLM class for interacting with Ollama models."""

    def __init__(self, model: str) -> None:
        super().__init__()
        self.model = model
        logger.info("OllamaLLM initialized with model", extra={"model": model})

    def call(self, prompt: str) -> str:
        """Call the Ollama model with a prompt."""
        logger.info("Calling Ollama model with prompt", extra={"model": self.model, "prompt": prompt})
        response = f"Ollama response to: {prompt}"  # Simulated response
        logger.debug("Ollama response", extra={"response": response})
        return response
