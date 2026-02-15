from documentassistent.agents.base_agent import BaseAgent, validate_state
from documentassistent.llm.base_llm import BaseLLM
from documentassistent.structure.pydantic_llm_calls.note_call import NoteExtraction
from documentassistent.structure.state import BaseWorkflowState, NoteExtractionState
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="NoteAgent",
    log_file="logs/note_agent.log",
)


class NoteAgent(BaseAgent):
    """Agent for extracting notes using LLMFactory."""

    def __init__(self, llm: BaseLLM | None = None) -> None:
        super().__init__(agent_name="NoteAgent", logger=logger, llm=llm)

    @validate_state
    def extract_note(self, state: BaseWorkflowState) -> NoteExtractionState:
        """Extract notes from the given text using the configured LLM."""
        state = self._convert_state(state, NoteExtractionState)
        result = self.llm.call(state, pydantic_object=NoteExtraction)
        logger.debug("Note extraction result: {}", result)
        return state.model_copy(update={"note_extraction_result": result})
