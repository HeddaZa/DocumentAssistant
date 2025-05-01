import openai

from llm.base_llm import BaseLLM
from utils.logger import setup_logger

logger = setup_logger(name="OpenAILLM")


class OpenAILLM(BaseLLM):
    """OpenAI LLM class for interacting with OpenAI models."""

    def __init__(self, api_key: str, model: str):
        super().__init__()
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        logger.info("OpenAILLM initialized with model: %s", model)

    def call(self, prompt: str) -> str:
        """Call the OpenAI model with a prompt."""
        logger.info("Calling OpenAI model '%s' with prompt: %s", self.model, prompt)
        try:
            response = openai.Completion.create(engine=self.model, prompt=prompt, max_tokens=100)
            result = response.choices[0].text.strip()
            logger.debug("OpenAI response: %s", result)
        except Exception:
            logger.exception("Error calling OpenAI API")
            raise
        else:
            return result
