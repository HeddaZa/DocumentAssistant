import openai

from llm.base_llm import BaseLLM


class OpenAILLM(BaseLLM):
    """OpenAI LLM class for interacting with OpenAI models."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def call(self, prompt: str) -> str:
        """Call the OpenAI model with a prompt."""
        response = openai.Completion.create(engine=self.model, prompt=prompt, max_tokens=100)
        return response.choices[0].text.strip()
