# UNIT 4: Human-in-the-Loop Patterns

# Exercise 4.1 - "Basic Oversight"
# Requirements:
# - Implement pre-execution approval flow
# - Add result review functionality
# - Implement approval tracking
# - Add notification system

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    pending_approvals: list[dict]
    approved_actions: list[dict]
    notifications: list[str]


def request_approval(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for requesting approval
    if not state.get("pending_approvals"):
        return {
            "messages": [],
            "pending_approvals": [{"action": "send_email", "status": "pending"}],
            "approved_actions": [],
            "notifications": [],
        }
    return state


def review_handler(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for handling reviews
    if state["pending_approvals"][0]["status"] == "pending":
        state["pending_approvals"][0]["status"] = "approved"
        state["approved_actions"].append({"action": "send_email"})
        return state
    return state


def notification_sender(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for sending notifications
    if state["approved_actions"]:
        state["notifications"].append("Email sent successfully!")
        return state
    return state


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
