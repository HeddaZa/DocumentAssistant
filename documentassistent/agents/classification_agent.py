from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.prompts.prompt_collection import CATEGORISATION_PROMPT
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
)
from documentassistent.structure.state import State
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

    def classify(self, state: State) -> State:
        """Classify the input text and return a Classification result."""
        if state is None:
            msg = "state must not be None"
            logger.error(msg)
            raise ValueError(msg)
        state.prompt = CATEGORISATION_PROMPT
        result = self.llm.call(state, pydantic_object=Classification)
        if not isinstance(result, Classification):
            msg = f"Expected Classification, got {type(result)}"
            raise TypeError(msg)
        logger.debug("Classification result: {}", result)
        return state.model_copy(
            update={
                "classification_result": result.label,
            },
        )
