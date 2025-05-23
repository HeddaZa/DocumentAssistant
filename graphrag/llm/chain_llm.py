from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
from llm.base_llm import BaseLLM
from structure.llm_call_structure import DocumentType
from structure.state import State
from utils.logger import setup_logger

logger = setup_logger(name="ChainLLM", log_file="logs/chain_llm.log")


class ChainLLM(BaseLLM):
    """Parent class for LLMs that use the chain pattern."""

    def __init__(self) -> None:
        super().__init__()
        self.llm = None
        self.chain = None

    def create_chain(self, prompt: str) -> None:
        """Create a chain for the LLM with the given prompt."""
        if not self.llm:
            msg = "LLM not initialized"
            raise ValueError(msg)

        pydantic_parser = PydanticOutputParser(pydantic_object=DocumentType)
        output_parser = OutputFixingParser.from_llm(
            parser=pydantic_parser,
            llm=self.llm,
        )
        prompt = PromptTemplate(
            template=prompt + "\n{format_instructions}",
            input_variables=[],
            partial_variables={
                "format_instructions": output_parser.get_format_instructions(),
            },
        )
        self.chain = prompt | self.llm | output_parser
        logger.debug("Chain created with prompt", extra={"prompt": prompt})

    def call(self, state: State) -> str:
        """Call the LLM with a prompt and state."""
        if not self.chain:
            self.create_chain(state.prompt)
        logger.debug("Calling chain with state", extra={"state": state})
        response = self.chain.invoke(
            {
                "text": state.text,
            },
            return_only_outputs=True,
        )
        return response
