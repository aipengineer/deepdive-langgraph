# UNIT 4: Human-in-the-Loop Patterns

# Exercise 4.3 - "Dynamic Routing"
# Requirements:
# - Implement human decision points
# - Add routing suggestions
# - Implement fallback paths
# - Add routing history

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    decision_points: list[dict]
    suggestions: list[str]
    routing_history: list[str]


def decision_handler(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for handling human decisions


def suggestion_generator(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for generating routing suggestions


def history_tracker(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for tracking routing history


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("decision_handler", decision_handler)
graph_builder.add_node("suggestion_generator", suggestion_generator)
graph_builder.add_node("history_tracker", history_tracker)

# Add the edges
graph_builder.add_edge(START, "decision_handler")
graph_builder.add_edge("decision_handler", "suggestion_generator")
graph_builder.add_edge("suggestion_generator", "history_tracker")

graph = graph_builder.compile()
