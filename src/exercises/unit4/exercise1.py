# UNIT 4: Human-in-the-Loop Patterns

# Exercise 4.1 - "Basic Oversight"
# Requirements:
# - Implement pre-execution approval flow
# - Add result review functionality
# - Implement approval tracking
# - Add notification system

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    pending_approvals: list[dict]
    approved_actions: list[dict]
    notifications: list[str]


def request_approval(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for requesting approval


def review_handler(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for handling reviews


def notification_sender(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for sending notifications


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("request_approval", request_approval)
graph_builder.add_node("review_handler", review_handler)
graph_builder.add_node("notification_sender", notification_sender)

# Add the edges
graph_builder.add_edge(START, "request_approval")
graph_builder.add_edge("request_approval", "review_handler")
graph_builder.add_edge("review_handler", "notification_sender")

graph = graph_builder.compile()
