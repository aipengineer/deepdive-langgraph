# UNIT 1: Graph Basics & State Management

# Exercise 1.3 - "Conditional Router"
# Requirements:
# - Create a graph with multiple response nodes
# - Implement a classifier node for message routing
# - Add at least 3 different response paths
# - Implement proper handling for ambiguous cases

from typing import Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float


def classifier_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for message classification
    message = state["messages"][-1].content
    if "hello" in message.lower():
        return {"classification": "greeting", "confidence": 0.9}
    elif "help" in message.lower():
        return {"classification": "help", "confidence": 0.8}
    else:
        return {"classification": "unknown", "confidence": 0.1}


def response_node_1(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for response path 1
    return {"messages": [HumanMessage(content="Hello there!")]}


def response_node_2(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for response path 2
    return {"messages": [HumanMessage(content="How can I help you?")]}


def response_node_3(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for response path 3
    return {"messages": [HumanMessage(content="I don't understand.")]}


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("classifier", classifier_node)
graph_builder.add_node("response_1", response_node_1)
graph_builder.add_node("response_2", response_node_2)
graph_builder.add_node("response_3", response_node_3)

# Add the edges with routing logic
graph_builder.add_edge(START, "classifier")
graph_builder.add_conditional_edges(
    "classifier",
    {
        lambda state: state["classification"] == "greeting": "response_1",
        lambda state: state["classification"] == "help": "response_2",
        lambda state: state["classification"] == "unknown": "response_3",
    },
)

graph = graph_builder.compile()
