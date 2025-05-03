from dotenv import load_dotenv

from llm.llm_factory import LLMFactory
from llm.ollama_llm import OllamaLLMCall
from load_config import load_config
from prompts.prompt_collection import CATEGORISATION_PROMPT
from structure.state import State
from utils.logger import setup_logger

load_dotenv()

logger = setup_logger(name="MyApp")


def main() -> str:
    """Loads configuration and creates LLM instance."""
    config = load_config("config.yaml")

    llm = LLMFactory.create_llm(config)
    logger.info("LLM instance created", extra={"llm_type": type(llm).__name__})

    prompt = "What is the capital of France?"
    response = llm.call(prompt)
    return response


if __name__ == "__main__":
    llm = OllamaLLMCall(model="gemma:7b")
    prompt = CATEGORISATION_PROMPT
    state = State(
        prompt=prompt,
        text="This is a test text for categorization. This is a receipt about 100EUR for a doctor.",
        result=None,
    )
    result = llm.call(state)
