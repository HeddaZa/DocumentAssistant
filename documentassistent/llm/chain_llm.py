from typing import TYPE_CHECKING, Any

from langchain.output_parsers import (
    OutputFixingParser,
    PydanticOutputParser,
)
from langchain.prompts import PromptTemplate

if TYPE_CHECKING:
    from langchain.schema.runnable import RunnableSequence

from documentassistent.exceptions import LLMError, LLMResponseError
from documentassistent.llm.base_llm import BaseLLM
from documentassistent.structure.state import State
from documentassistent.utils.langfuse_handler import LangfuseHandler
from documentassistent.utils.logger import setup_logger

logger = setup_logger(name="ChainLLM", log_file="logs/chain_llm.log")

langfuse = LangfuseHandler()


class ChainLLM(BaseLLM):
    """Base class for LLM chains."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model
        super().__init__()
        self.llm: Any = None
        self.chain: RunnableSequence[dict[str, str], Any] | None = None
        self._current_pydantic_type: type | None = None

    def create_chain(self, prompt: str, pydantic_object: type) -> None:
        """Create a chain for the LLM with the given prompt and pydantic object."""
        if not self.llm:
            msg = "LLM not initialized"
            raise LLMError(msg)

        try:
            pydantic_parser: PydanticOutputParser = PydanticOutputParser(
                pydantic_object=pydantic_object,
            )
            output_parser = OutputFixingParser.from_llm(
                parser=pydantic_parser,
                llm=self.llm,
            )
            full_prompt = PromptTemplate(
                template=prompt + "\n{format_instructions}",
                input_variables=[],
                partial_variables={
                    "format_instructions": output_parser.get_format_instructions(),
                },
            )
            self.chain = full_prompt | self.llm | output_parser
            logger.debug("Chain created with prompt", extra={"prompt": full_prompt})
        except Exception as e:
            msg = f"Chain creation failed: {e!s}"
            logger.exception(msg)
            raise LLMError(msg) from e

    @langfuse.trace()
    def call(self, state: State, pydantic_object: type, **kwargs: Any) -> Any:
        """Call the LLM with a prompt, state, and pydantic object."""
        # Recreate chain if pydantic_object changed or chain doesn't exist
        if not self.chain or self._current_pydantic_type != pydantic_object:
            self.create_chain(state.prompt, pydantic_object)
            self._current_pydantic_type = pydantic_object
            if not self.chain:
                msg = "Chain creation failed to initialize chain"
                raise LLMError(msg)

        logger.debug("Calling chain with state", extra={"state": state})
        response = self.chain.invoke(
            {"text": state.text},
            **kwargs,
        )
        if not isinstance(response, pydantic_object):
            msg = f"Unexpected response type: {type(response)}"
            logger.error(msg)
            raise LLMResponseError(msg)

        return response
