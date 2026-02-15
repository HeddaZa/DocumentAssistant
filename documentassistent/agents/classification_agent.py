from documentassistent.agents.base_agent import BaseAgent, validate_state
from documentassistent.llm.base_llm import BaseLLM
from documentassistent.structure.pydantic_llm_calls.classification_call import (
    Classification,
)
from documentassistent.structure.state import BaseWorkflowState, ClassificationState
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="ClassificationAgent",
    log_file="logs/classification_agent.log",
)


class ClassificationAgent(BaseAgent):
    """
    Agent for document classification using LLMFactory and custom prompt/structure.

    This agent uses a factory to instantiate the LLM, a custom prompt, and a
    Pydantic structure for classification tasks.
    """

    def __init__(self, llm: BaseLLM | None = None) -> None:
        super().__init__(agent_name="ClassificationAgent", logger=logger, llm=llm)

    @validate_state
    def classify(self, state: BaseWorkflowState) -> ClassificationState:
        """Classify the input text and return a Classification result."""
        state = self._convert_state(state, ClassificationState)
        result = self.llm.call(state, pydantic_object=Classification)
        logger.debug("Classification result: {}", result)
        return state.model_copy(update={"classification_result": result})
