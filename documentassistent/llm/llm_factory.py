from typing import ClassVar, TypedDict

from documentassistent.exceptions import UnsupportedProviderError
from documentassistent.llm.base_llm import BaseLLM
from documentassistent.llm.ollama_llm import OllamaLLMCall
from documentassistent.llm.openai_llm import OpenAILLM
from documentassistent.utils.logger import setup_logger

logger = setup_logger(name="LLMFactory", log_file="logs/llm_factory.log")


class LLMConfig(TypedDict):
    """Configuration for the LLM."""

    type: str
    model: str | None


class ConfigDict(TypedDict):
    """Configuration dictionary containing LLM configuration."""

    llm: LLMConfig


class LLMFactory:
    """Factory class to create LLM instances based on configuration."""

    _llm_classes: ClassVar[dict[str, type[BaseLLM]]] = {
        "ollama": OllamaLLMCall,
        "openai": OpenAILLM,
    }

    @classmethod
    def create_llm(cls, config: ConfigDict) -> BaseLLM:
        """Create an LLM instance based on the config."""
        llm_type = config["llm"]["type"]
        llm_class = cls._llm_classes.get(llm_type)

        if not llm_class:
            msg = f"Unsupported LLM type: {llm_type!r}"
            logger.error(msg)
            raise UnsupportedProviderError(msg)

        # Create instance with optional model parameter
        model = config["llm"].get("model")
        llm = llm_class(model=model) if model else llm_class()

        logger.info("Created LLM instance", extra={"type": llm_type})
        return llm
