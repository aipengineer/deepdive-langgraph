# UNIT 1: Graph Basics & State Management

# Exercise 1.3 - "Conditional Router"
# Requirements:
# - Create a graph with multiple response nodes
# - Implement a classifier node for message routing
# - Add at least 3 different response paths
# - Implement proper handling for ambiguous cases

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float


def classifier_node(state: State) -> State:
    """Classify incoming messages to determine response path."""
    message = state["messages"][-1].content

    # Return classification without modifying messages
    if "hello" in message.lower():
        return {
            "messages": state["messages"],  # Keep existing messages
            "classification": "greeting",
            "confidence": 0.9
        }
    elif "help" in message.lower():
        return {
            "messages": state["messages"],  # Keep existing messages
            "classification": "help",
            "confidence": 0.8
        }
    else:
        return {
            "messages": state["messages"],  # Keep existing messages
            "classification": "unknown",
            "confidence": 0.1
        }


def response_node_1(state: State) -> State:
    """Handle greeting responses."""
    return {
        "messages": [AIMessage(content="Hello there!")],
        "classification": state["classification"],
        "confidence": state["confidence"]
    }


def response_node_2(state: State) -> State:
    """Handle help requests."""
    return {
        "messages": [AIMessage(content="How can I help you?")],
        "classification": state["classification"],
        "confidence": state["confidence"]
    }


def response_node_3(state: State) -> State:
    """Handle unknown messages."""
    return {
        "messages": [AIMessage(content="I don't understand.")],
        "classification": state["classification"],
        "confidence": state["confidence"]
    }


def get_next_node(state: State) -> str:
    """Determine the next node based on message classification."""
    classification = state["classification"]

    if classification == "greeting":
        return "response_1"
    elif classification == "help":
        return "response_2"
    else:
        return "response_3"


# Initialize the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("classifier", classifier_node)
graph_builder.add_node("response_1", response_node_1)
graph_builder.add_node("response_2", response_node_2)
graph_builder.add_node("response_3", response_node_3)

# Connect nodes
graph_builder.add_edge(START, "classifier")

# Add conditional edges from classifier to responses
graph_builder.add_conditional_edges(
    "classifier",
    get_next_node,
    {
        "response_1": "response_1",
        "response_2": "response_2",
        "response_3": "response_3"
    }
)

# Add edges from responses to END
graph_builder.add_edge("response_1", END)
graph_builder.add_edge("response_2", END)
graph_builder.add_edge("response_3", END)

# Compile the graph
graph = graph_builder.compile()

# Default input for testing
default_input = {"messages": [], "classification": "", "confidence": 0.0}

# Make variables available for testing
__all__ = ["graph", "default_input"]