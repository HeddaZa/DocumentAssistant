from enum import Enum
from typing import Any

from langgraph.graph import END, StateGraph

from documentassistent.agents.classification_agent import ClassificationAgent
from documentassistent.agents.invoice_agent import InvoiceAgent
from documentassistent.agents.note_agent import NoteAgent
from documentassistent.agents.result_agent import ResultAgent
from documentassistent.agents.storage_agent import StorageAgent
from documentassistent.structure.state import State
from documentassistent.utils.logger import setup_logger

logger = setup_logger(
    name="Graph",
    log_file="logs/graph.log",
)


class AgentNames(Enum):
    """Enumeration for agent names used in the graph."""

    CLASSIFICATION = "classification_agent"
    INVOICE = "invoice_agent"
    NOTE = "note_agent"
    RESULT = "result_agent"
    STORAGE = "storage_agent"


def create_graph() -> Any:
    """Create a StateGraph with agents."""
    logger.info("Creating StateGraph with agents... 🧩")
    classification_agent = ClassificationAgent()
    invoice_agent = InvoiceAgent()
    note_agent = NoteAgent()
    result_agent = ResultAgent()
    storage_agent = StorageAgent()

    builder = StateGraph(State)

    builder.add_node(
        AgentNames.CLASSIFICATION.value,
        classification_agent.classify,
    )
    builder.add_node(
        AgentNames.INVOICE.value,
        invoice_agent.extract_invoice,
    )
    builder.add_node(AgentNames.NOTE.value, note_agent.extract_note)
    builder.add_node(AgentNames.RESULT.value, result_agent.extract_result)
    builder.add_node(AgentNames.STORAGE.value, storage_agent.store_results)

    builder.set_entry_point(AgentNames.CLASSIFICATION.value)

    # Conditional routing based on classification_result
    builder.add_conditional_edges(
        AgentNames.CLASSIFICATION.value,
        lambda state: state.classification_result.label.value,
        {
            "invoice": AgentNames.INVOICE.value,
            "note": AgentNames.NOTE.value,
            "result": AgentNames.RESULT.value,
        },
    )

    # All extraction agents flow to storage
    builder.add_edge(AgentNames.INVOICE.value, AgentNames.STORAGE.value)
    builder.add_edge(AgentNames.NOTE.value, AgentNames.STORAGE.value)
    builder.add_edge(AgentNames.RESULT.value, AgentNames.STORAGE.value)

    # Storage is the terminal node
    builder.add_edge(AgentNames.STORAGE.value, END)

    graph = builder.compile()
    logger.success("StateGraph created successfully. 🎉")
    return graph


if __name__ == "__main__":
    # Example usage of the graph
    graph = create_graph()
    initial_state = State(
        prompt="Classify this document",
        text="Sample text for classification. Doctors receipt of 100EUR",
    )
    result_state = graph.invoke(initial_state)
    logger.info("Final state after processing: {}", result_state)
