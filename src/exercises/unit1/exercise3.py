# UNIT 1: Graph Basics & State Management

# Exercise 1.3 - "Conditional Router"
# Requirements:
# - Create a graph with multiple response nodes
# - Implement a classifier node for message routing
# - Add at least 3 different response paths
# - Implement proper handling for ambiguous cases

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float


def classifier_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for message classification


def response_node_1(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for response path 1


def response_node_2(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for response path 2


def response_node_3(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for response path 3


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("classifier", classifier_node)
graph_builder.add_node("response_1", response_node_1)
graph_builder.add_node("response_2", response_node_2)
graph_builder.add_node("response_3", response_node_3)

# Add the edges
# You must implement the conditional edges with routing logic
# based on the classification result

graph = graph_builder.compile()
