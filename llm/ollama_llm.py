from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from llm.base_llm import BaseLLM
from structure.llm_call_structure import DocumentType
from structure.state import State
from utils.logger import setup_logger

logger = setup_logger(name="OllamaLLM", log_file="logs/ollama_llm.log")


class OllamaLLMCall(BaseLLM):
    """Ollama LLM class for interacting with Ollama models."""

    def __init__(self, model: str = "gemma") -> None:
        super().__init__()
        self.llm = OllamaLLM(model=model)
        self.chain = None
        logger.info("OllamaLLM initialized with model", extra={"model": model})

    def create_chain(self, prompt: str) -> None:
        """Create a chain for the LLM with the given prompt."""
        pydantic_parser = PydanticOutputParser(pydantic_object=DocumentType)
        output_parser = OutputFixingParser.from_llm(
            parser=pydantic_parser,
            llm=self.llm,
        )
        prompt = PromptTemplate(
            template=prompt + "\n{format_instructions}",
            input_variables=[],
            partial_variables={"format_instructions": output_parser.get_format_instructions()},
        )
        self.chain = prompt | self.llm | output_parser
        logger.debug("Chain created with prompt", extra={"prompt": prompt})

    def call(self, state: State) -> str:
        """Call the Ollama model with a prompt."""
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
