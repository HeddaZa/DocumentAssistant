from llm.base_llm import BaseLLM


class OllamaLLM(BaseLLM):
    """Ollama LLM class for interacting with Ollama models."""

    def __init__(self, model: str) -> None:
        self.model = model

    def call(self, prompt: str) -> str:
        """Call the Ollama model with a prompt."""
        return f"Ollama response to: {prompt}"
