# UNIT 3: Checkpointing & Persistence

# Exercise 3.1 - "Checkpoint Basics"
# Requirements:
# - Implement basic checkpointing with MemorySaver
# - Add state versioning
# - Implement reload from checkpoint
# - Add checkpoint cleanup logic

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    version: str
    metadata: dict[str, Any]


def chat_completion_checkpointed(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for saving and restoring state
    if state.get("messages"):
        return {"messages": [], "version": "v1", "metadata": {"last_restored": False}}
    return {"messages": [], "version": "v1", "metadata": {"last_restored": True}}


def cleanup_checkpointed(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for cleaning up old states
    if state["metadata"].get("last_restored"):
        return {"metadata": {"last_restored": False, "old_states_cleaned_up": False}}
    return {"metadata": {"old_states_cleaned_up": True}}


# Initialize the graph
graph_builder = StateGraph(State)

# Add the node
graph_builder.add_node("chat_completion", chat_completion_checkpointed)

# Add the cleanup node
graph_builder.add_node("cleanup", cleanup_checkpointed)

# Add the edges
graph_builder.add_edge(START, "chat_completion")
graph_builder.add_edge("chat_completion", "cleanup")
graph_builder.add_edge("cleanup", "chat_completion")

graph = graph_builder.compile()
