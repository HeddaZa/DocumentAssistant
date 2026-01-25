from documentassistent.agents.base_agent import BaseAgent, validate_state
from documentassistent.llm.base_llm import BaseLLM
from documentassistent.structure.pydantic_llm_calls.result_call import ResultExtraction
from documentassistent.structure.state import BaseWorkflowState, ResultExtractionState
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="ResultAgent",
    log_file="logs/result_agent.log",
)


class ResultAgent(BaseAgent):
    """Agent for extracting medical test results using LLMFactory."""

    def __init__(self, llm: BaseLLM | None = None) -> None:
        super().__init__(agent_name="ResultAgent", logger=logger, llm=llm)

    @validate_state
    def extract_result(self, state: BaseWorkflowState) -> ResultExtractionState:
        """Extract medical test results from the given text using the configured LLM."""
        state = self._convert_state(state, ResultExtractionState)
        result = self.llm.call(state, pydantic_object=ResultExtraction)
        logger.debug("Result extraction result: {}", result)
        return state.model_copy(update={"result_extraction_result": result})
