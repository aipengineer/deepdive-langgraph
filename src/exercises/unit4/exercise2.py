# UNIT 4: Human-in-the-Loop Patterns

# Exercise 4.2 - "State Editor"
# Requirements:
# - Implement state modification UI
# - Add validation for edits
# - Implement edit history
# - Add rollback functionality

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    edits: list[dict]
    validators: dict[str, Any]
    history: list[dict]


def edit_handler(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for handling state edits


def validation_logic(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for validating state edits


def history_tracker(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for tracking edit history


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("edit_handler", edit_handler)
graph_builder.add_node("validation_logic", validation_logic)
graph_builder.add_node("history_tracker", history_tracker)

# Add the edges
graph_builder.add_edge(START, "edit_handler")
graph_builder.add_edge("edit_handler", "validation_logic")
graph_builder.add_edge("validation_logic", "history_tracker")

graph = graph_builder.compile()
