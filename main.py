from dotenv import load_dotenv

from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.prompts.prompt_collection import CATEGORISATION_PROMPT
from documentassistent.structure.state import State
from documentassistent.utils.logger import setup_logger
from load_config import load_config

load_dotenv()

logger = setup_logger(name="MyApp", log_file="logs/app.log")
CONFIG = load_config("config.yaml")


def main(text: str) -> None:
    """Load configuration and process text with LLM."""
    config: ConfigDict = {
        "llm": {
            "type": "ollama",
            "model": CONFIG["ollama"]["model"],
        },
    }

    llm = LLMFactory.create_llm(config)
    logger.info("LLM instance created", extra={"llm_type": type(llm).__name__})

    state = State(
        prompt=CATEGORISATION_PROMPT,
        text=text,
        result=None,
    )
    result = llm.call(state)
    logger.debug("Full result details: {}", result)


if __name__ == "__main__":
    text = """
This is a test text for categorization. This is a receipt about 100EUR for a doctor.
"""
    main(text=text)
