import os

from langchain_openai import ChatOpenAI  # type: ignore[import-not-found]
from pydantic import SecretStr  # type: ignore[import-not-found]

from graphrag.llm.chain_llm import ChainLLM
from graphrag.utils.logger import setup_logger

logger = setup_logger(name="OpenAILLM", log_file="logs/openai_llm.log")


class OpenAILLM(ChainLLM):
    """OpenAI LLM class for interacting with OpenAI models."""

    def __init__(self) -> None:
        super().__init__()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        if not self.api_key:
            msg = "OPENAI_API_KEY not found in environment variables"
            raise ValueError(msg)
        self.llm = ChatOpenAI(
            api_key=SecretStr(self.api_key),
            model=self.model,
        )
        logger.info("OpenAILLM initialized with model: {}", self.model)
