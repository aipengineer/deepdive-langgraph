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
    # Implement the logic for handling human decisions
    if not state.get("decision_points"):
        return {
            "messages": [],
            "decision_points": [
                {"question": "Which path to take?", "options": ["A", "B"]}
            ],
            "suggestions": [],
            "routing_history": [],
        }
    elif state["decision_points"][0]["question"] == "Which path to take?":
        if state["messages"][0].content == "A":
            state["decision_points"] = [
                {"question": "Are you sure?", "options": ["Yes", "No"]}
            ]
            state["routing_history"].append("A")
        else:
            state["decision_points"] = []
            state["routing_history"].append("B")
        return state
    elif state["decision_points"][0]["question"] == "Are you sure?":
        if state["messages"][1].content == "Yes":
            state["decision_points"] = []
            state["routing_history"].append("A")
        else:
            state["decision_points"] = []
            state["routing_history"].append("B")  # Fallback to B
        return state
    return state


def suggestion_generator(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for generating routing suggestions
    if state["decision_points"]:
        question = state["decision_points"][0]["question"]
        if question == "Which path to take?":
            state["suggestions"].append("Path A is recommended.")
        elif question == "Are you sure?":
            state["suggestions"].append("Think carefully.")
        return state
    return state


def history_tracker(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for tracking routing history
    return state  # No additional tracking needed


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
