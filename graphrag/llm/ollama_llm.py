from langchain_ollama import OllamaLLM

from graphrag.llm.chain_llm import ChainLLM
from graphrag.utils.logger import setup_logger

logger = setup_logger(name="OllamaLLM", log_file="logs/ollama_llm.log")


class OllamaLLMCall(ChainLLM):
    """Ollama LLM class for interacting with Ollama models."""

    def __init__(self, model: str = "gemma") -> None:
        super().__init__(model=model)
        self.llm = OllamaLLM(model=model)
        logger.info("OllamaLLM initialized with model", extra={"model": model})
