from typing import TYPE_CHECKING, Any

from langchain.output_parsers import (
    OutputFixingParser,
    PydanticOutputParser,
)
from langchain.prompts import PromptTemplate

if TYPE_CHECKING:
    from langchain.schema.runnable import RunnableSequence

from graphrag.llm.base_llm import BaseLLM
from graphrag.structure.llm_call_structure import DocumentType
from graphrag.structure.state import State
from graphrag.utils.langfuse_handler import LangfuseHandler
from graphrag.utils.logger import setup_logger

logger = setup_logger(name="ChainLLM", log_file="logs/chain_llm.log")

langfuse = LangfuseHandler()


class ChainCreationError(Exception):
    """Custom exception for chain creation errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ChainLLM(BaseLLM):
    """Base class for LLM chains."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model
        super().__init__()
        self.llm: Any = None
        self.chain: RunnableSequence[dict[str, str], DocumentType] | None = None

    def create_chain(self, prompt: str) -> None:
        """Create a chain for the LLM with the given prompt."""
        if not self.llm:
            msg = "LLM not initialized"
            raise ValueError(msg)

        try:
            pydantic_parser = PydanticOutputParser(pydantic_object=DocumentType)
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
            raise ChainCreationError(msg) from e

    @langfuse.trace()
    def call(self, state: State) -> DocumentType:
        """Call the LLM with a prompt and state."""
        if not self.chain:
            self.create_chain(state.prompt)
            if not self.chain:
                msg = "Chain creation failed to initialize chain"
                raise ChainCreationError(msg)

        logger.debug("Calling chain with state", extra={"state": state})
        response = self.chain.invoke(
            {"text": state.text},
            return_only_outputs=True,
        )
        if not isinstance(response, DocumentType):
            msg = f"Unexpected response type: {type(response)}"
            logger.error(msg)
            raise TypeError(msg)

        return response
