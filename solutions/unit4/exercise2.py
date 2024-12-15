# UNIT 4: Human-in-the-Loop Patterns

# Exercise 4.2 - "State Editor"
# Requirements:
# - Implement state modification UI
# - Add validation for edits
# - Implement edit history
# - Add rollback functionality

from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    edits: list[dict]
    validators: dict[str, Any]
    history: list[dict]


def edit_handler(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for handling state edits
    if not state.get("edits"):
        return {
            "messages": [],
            "edits": [{"field": "message", "new_value": "Hello world!"}],
            "validators": {"message": lambda x: len(x) <= 20},
            "history": [],
        }
    return state


def validation_logic(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for validating state edits
    for edit in state["edits"]:
        field = edit["field"]
        new_value = edit["new_value"]
        if state["validators"][field](new_value):
            state["messages"].append(HumanMessage(content=new_value))
        else:
            raise ValueError(f"Invalid edit for field: {field}")
    return state


def history_tracker(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for tracking edit history
    state["history"].append({"messages": state["messages"].copy()})
    return state


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
