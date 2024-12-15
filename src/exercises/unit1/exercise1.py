# UNIT 1: Graph Basics & State Management

# Exercise 1.1 - "Hello LangGraph"
# Requirements:
# - Create a StateGraph with a single LLM node
# - Define a basic State type using TypedDict and Annotated
# - Implement proper input/output message handling
# - Include basic error handling for API failures

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def llm_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for the LLM node


# Initialize the graph
graph_builder = StateGraph(State)

# Add the node
graph_builder.add_node("llm", llm_node)

# Add the edges
graph_builder.add_edge(START, "llm")

graph = graph_builder.compile()
