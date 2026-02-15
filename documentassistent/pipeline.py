"""Document processing pipeline using LangChain LCEL."""

from typing import Any

from langchain_core.runnables import RunnableBranch, RunnableLambda

from documentassistent.agents.classification_agent import ClassificationAgent
from documentassistent.agents.invoice_agent import InvoiceAgent
from documentassistent.agents.note_agent import NoteAgent
from documentassistent.agents.result_agent import ResultAgent
from documentassistent.agents.storage_agent import StorageAgent
from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.structure.state import ClassificationState
from documentassistent.utils.logger import setup_logger
from load_config import load_config

logger = setup_logger(
    name="Pipeline",
    log_file="logs/pipeline.log",
)
CONFIG = load_config("config.yaml")


def create_pipeline(
    classification_agent: ClassificationAgent | None = None,
    invoice_agent: InvoiceAgent | None = None,
    note_agent: NoteAgent | None = None,
    result_agent: ResultAgent | None = None,
    storage_agent: StorageAgent | None = None,
) -> Any:
    """
    Create a document processing pipeline using LangChain LCEL.

    Args:
        classification_agent: Optional classification agent. If None, creates default.
        invoice_agent: Optional invoice extraction agent. If None, creates default.
        note_agent: Optional note extraction agent. If None, creates default.
        result_agent: Optional result extraction agent. If None, creates default.
        storage_agent: Optional storage agent. If None, creates default.

    Returns:
        Compiled LCEL chain ready for execution.

    Example:
        # Production usage with defaults
        pipeline = create_pipeline()
        result = pipeline.invoke(state)

        # Testing with mock agents
        pipeline = create_pipeline(
            classification_agent=MockClassificationAgent(),
            storage_agent=MockStorageAgent(),
        )
    """
    logger.info("Creating LCEL pipeline... 🧩")

    # Create default agents if not provided
    if (
        classification_agent is None
        or invoice_agent is None
        or note_agent is None
        or result_agent is None
    ):
        # Create LLM once for all agents that need it (dependency injection)
        provider = CONFIG.get("llm", {}).get("provider", "ollama")
        model = CONFIG.get("llm", {}).get(
            "model",
            CONFIG.get(provider, {}).get("model"),
        )
        config: ConfigDict = {
            "llm": {
                "type": provider,
                "model": model,
            },
        }
        llm = LLMFactory.create_llm(config)
        logger.info(
            "Created shared LLM instance",
            extra={"type": provider, "model": model},
        )

        # Create default agents for any that weren't provided
        if classification_agent is None:
            classification_agent = ClassificationAgent(llm=llm)
        if invoice_agent is None:
            invoice_agent = InvoiceAgent(llm=llm)
        if note_agent is None:
            note_agent = NoteAgent(llm=llm)
        if result_agent is None:
            result_agent = ResultAgent(llm=llm)

    if storage_agent is None:
        storage_agent = StorageAgent()

    # Helper functions for type-safe branching
    def is_invoice(state: ClassificationState) -> bool:
        """Check if state is classified as invoice."""
        return (
            state.classification_result is not None
            and state.classification_result.label.value == "invoice"
        )

    def is_note(state: ClassificationState) -> bool:
        """Check if state is classified as note."""
        return (
            state.classification_result is not None
            and state.classification_result.label.value == "note"
        )

    # Wrap agent methods as RunnableLambda
    classification_runnable = RunnableLambda(classification_agent.classify)
    invoice_runnable = RunnableLambda(invoice_agent.extract_invoice)
    note_runnable = RunnableLambda(note_agent.extract_note)
    result_runnable = RunnableLambda(result_agent.extract_result)
    storage_runnable = RunnableLambda(storage_agent.store_results)

    # Create conditional branch for extraction based on classification
    extraction_branch: RunnableBranch[ClassificationState, ClassificationState] = (
        RunnableBranch(
            (is_invoice, invoice_runnable),
            (is_note, note_runnable),
            result_runnable,
        )
    )

    # Create the full pipeline: classify -> extract -> store
    pipeline = classification_runnable | extraction_branch | storage_runnable

    logger.success("LCEL pipeline created successfully. 🎉")
    return pipeline


if __name__ == "__main__":
    # Example usage of the pipeline
    pipeline = create_pipeline()
    initial_state = ClassificationState(
        text="Sample text for classification. Doctors receipt of 100EUR",
    )
    result_state = pipeline.invoke(initial_state)
    logger.info("Final state after processing: {}", result_state)
