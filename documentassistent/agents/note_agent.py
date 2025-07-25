from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.prompts.prompt_collection import NOTE_EXTRACTION_PROMPT
from documentassistent.structure.pydantic_llm_calls.note_call import NoteExtraction
from documentassistent.structure.state import State
from documentassistent.utils.logger import setup_logger
from load_config import load_config

logger = setup_logger(
    name="NoteAgent",
    log_file="logs/note_agent.log",
)
CONFIG = load_config("config.yaml")


class NoteAgent:
    """Agent for extracting notes using LLMFactory."""

    def __init__(self) -> None:
        config: ConfigDict = {
            "llm": {
                "type": "ollama",
                "model": CONFIG["ollama"]["model"],
            },
        }
        self.llm = LLMFactory.create_llm(config)
        logger.info(
            "NoteAgent initialized with LLM",
            extra={"llm_type": type(self.llm).__name__},
        )

    def extract_note(self, state: State) -> State:
        """Extract notes from the given text using the configured LLM."""
        if state is None:
            msg = "state must not be None"
            raise ValueError(msg)
        state.prompt = NOTE_EXTRACTION_PROMPT
        result = self.llm.call(state, pydantic_object=NoteExtraction)
        if not isinstance(result, NoteExtraction):
            msg = f"Expected NoteExtraction, got {type(result)}"
            raise TypeError(msg)
        logger.debug("Note extraction result: {}", result)
        return state.model_copy(
            update={
                "note_extraction_result": result,
            },
        )
