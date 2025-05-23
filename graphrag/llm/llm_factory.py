from typing import ClassVar

from llm.base_llm import BaseLLM
from llm.ollama_llm import OllamaLLMCall
from llm.openai_llm import OpenAILLM
from utils.logger import setup_logger

logger = setup_logger(name="LLMFactory", log_file="logs/llm_factory.log")


class LLMFactory:
    """Factory class to create LLM instances based on configuration."""

    _llm_classes: ClassVar[dict[str, type[BaseLLM]]] = {
        "ollama": OllamaLLMCall,
        "openai": OpenAILLM,
    }

    @classmethod
    def create_llm(cls, config: dict[str, str]) -> BaseLLM:
        """Create an LLM instance based on the config."""
        llm_type = config["llm"]["type"]
        llm_class = cls._llm_classes.get(llm_type)

        if not llm_class:
            msg = f"Unsupported LLM type: {llm_type!r}"
            logger.error(msg)
            raise ValueError(msg)

        if llm_type == "ollama":
            llm = llm_class(model=config["llm"]["model"])
        elif llm_type == "openai":
            llm = llm_class()

        logger.info("Created LLM instance", extra={"type": llm_type})
        return llm
