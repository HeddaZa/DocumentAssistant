import os

from langchain_openai import ChatOpenAI

from llm.chain_llm import ChainLLM
from utils.logger import setup_logger

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
            openai_api_key=self.api_key,
            model_name=self.model,
        )
        logger.info("OpenAILLM initialized with model: {}", self.model)
