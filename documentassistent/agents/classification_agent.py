from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.prompts.prompt_collection import CATEGORISATION_PROMPT
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
)
from documentassistent.structure.state import LLMCall, State
from documentassistent.utils.logger import setup_logger
from load_config import load_config

logger = setup_logger(
    name="ClassificationAgent",
    log_file="logs/classification_agent.log",
)
CONFIG = load_config("config.yaml")


class ClassificationAgent:
    """
    Agent for document classification using LLMFactory and custom prompt/structure.

    This agent uses a factory to instantiate the LLM, a custom prompt, and a
    Pydantic structure for classification tasks.
    """

    def __init__(self) -> None:
        config: ConfigDict = {
            "llm": {
                "type": "ollama",
                "model": CONFIG["ollama"]["model"],
            },
        }
        self.llm = LLMFactory.create_llm(config)
        logger.info(
            "ClassificationAgent initialized with LLM",
            extra={"llm_type": type(self.llm).__name__},
        )

    def classify(self, text: str) -> Classification:
        """Classify the input text and return a Classification result."""
        state = State(
            prompt=CATEGORISATION_PROMPT,
            text=text,
            result=None,
        )
        llm_call = LLMCall(
            prompt=CATEGORISATION_PROMPT,
            pydantic_object=Classification,
            state=state,
        )
        if llm_call.state is None:
            msg = "LLMCall.state must not be None"
            raise ValueError(msg)
        result = self.llm.call(llm_call.state, pydantic_object=Classification)
        if not isinstance(result, Classification):
            msg = f"Expected Classification, got {type(result)}"
            raise TypeError(msg)
        logger.debug("Classification result: {}", result)
        return result
