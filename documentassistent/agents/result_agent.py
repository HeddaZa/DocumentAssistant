from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.prompts.prompt_collection import RESULT_EXTRACTION_PROMPT
from documentassistent.structure.pydantic_llm_calls.result_call import ResultExtraction
from documentassistent.structure.state import LLMCall, State
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

    def extract_result(self, text: str) -> ResultExtraction:
        """Extract medical test results from the given text using the configured LLM."""
        state = State(
            prompt=RESULT_EXTRACTION_PROMPT,
            text=text,
            result=None,
        )
        llm_call = LLMCall(
            prompt=RESULT_EXTRACTION_PROMPT,
            pydantic_object=ResultExtraction,
            state=state,
        )
        if llm_call.state is None:
            msg = "LLMCall.state must not be None"
            raise ValueError(msg)
        result = self.llm.call(llm_call.state, pydantic_object=ResultExtraction)
        if not isinstance(result, ResultExtraction):
            msg = f"Expected ResultExtraction, got {type(result)}"
            raise TypeError(msg)
        logger.debug("Result extraction result: {}", result)
        return result
