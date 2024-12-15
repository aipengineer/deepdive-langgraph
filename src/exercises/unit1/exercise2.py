# UNIT 1: Graph Basics & State Management

# Exercise 1.2 - "Message Memory"
# Requirements:
# - Extend Exercise 1.1 to maintain conversation context
# - Add a message summarization node for long conversations
# - Implement a configurable message window size
# - Add metadata to messages (timestamps, roles, etc.)

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int


def llm_response(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for generating LLM responses


def message_windowing(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for managing message window


def summary_generation(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for generating conversation summaries


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("llm_response", llm_response)
graph_builder.add_node("message_windowing", message_windowing)
graph_builder.add_node("summary_generation", summary_generation)

# Add the edges
graph_builder.add_edge(START, "llm_response")
graph_builder.add_edge("llm_response", "message_windowing")
graph_builder.add_edge("message_windowing", "summary_generation")

graph = graph_builder.compile()
