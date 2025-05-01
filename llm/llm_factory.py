from llm.base_llm import BaseLLM
from llm.ollama_llm import OllamaLLM
from llm.openai_llm import OpenAILLM


class LLMFactory:
    """Factory class to create LLM instances based on configuration."""

    @staticmethod
    def create_llm(config: dict) -> BaseLLM:
        """Create an LLM instance as Factory method based on the config.

        Args:
            config (dict): Configuration dictionary.

        Returns:
            BaseLLM: An instance of a class implementing BaseLLM.
        """
        llm_type = config["llm"]["type"]
        if llm_type == "ollama":
            return OllamaLLM(model=config["llm"]["model"])
        if llm_type == "openai":
            return OpenAILLM(api_key=config["llm"]["api_key"], model=config["llm"]["model"])
        msg = f"Unsupported LLM type: {llm_type!r}"
        raise ValueError(msg)
