from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.structure.pydantic_llm_calls.result_call import ResultExtraction
from documentassistent.structure.state import State
from documentassistent.utils.logger import setup_logger
from load_config import load_config

logger = setup_logger(
    name="ResultAgent",
    log_file="logs/result_agent.log",
)
CONFIG = load_config("config.yaml")


class ResultAgent:
    """Agent for extracting medical test results using LLMFactory."""

    def __init__(self) -> None:
        config: ConfigDict = {
            "llm": {
                "type": "ollama",
                "model": CONFIG["ollama"]["model"],
            },
        }
        self.llm = LLMFactory.create_llm(config)
        logger.info(
            "ResultAgent initialized with LLM",
            extra={"llm_type": type(self.llm).__name__},
        )

    def extract_result(self, state: State) -> State:
        """Extract medical test results from the given text using the configured LLM."""
        if state is None:
            msg = "state must not be None"
            raise ValueError(msg)
        result = self.llm.call(state, pydantic_object=ResultExtraction)
        if not isinstance(result, ResultExtraction):
            msg = f"Expected ResultExtraction, got {type(result)}"
            raise TypeError(msg)
        logger.debug("Result extraction result: {}", result)
        return state.model_copy(
            update={
                "result_extraction_result": result,
            },
        )
