# UNIT 2: Building Agents with LangGraph

# Exercise 2.3 - "Parallel Tool Executor"
# Requirements:
# - Implement parallel tool execution
# - Add result aggregation logic
# - Implement proper error handling for partial failures
# - Include progress reporting

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict]
    results: dict[str, Any]
    errors: dict[str, str]


def parallel_executor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for parallel tool execution


def result_aggregator(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for aggregating tool results


def error_handler(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for handling tool errors


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("parallel_executor", parallel_executor)
graph_builder.add_node("result_aggregator", result_aggregator)
graph_builder.add_node("error_handler", error_handler)

# Add the edges
graph_builder.add_edge(START, "parallel_executor")
# You must implement the edges for result aggregation and error handling

graph = graph_builder.compile()
