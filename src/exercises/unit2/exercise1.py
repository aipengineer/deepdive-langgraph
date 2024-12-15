# UNIT 2: Building Agents with LangGraph

# Exercise 2.1 - "Simple Tool User"
# Requirements:
# - Create a graph that integrates with TavilySearchResults tool
# - Implement proper tool calling with JSON validation
# - Add retry logic for failed tool calls
# - Include proper error messaging to users

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


def llm_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for the LLM node with tool binding


def tool_executor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for executing the tool


def result_processor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for processing tool results


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_executor", tool_executor)
graph_builder.add_node("result_processor", result_processor)

# Add the edges
graph_builder.add_edge(START, "llm")
# You must implement the edges for tool execution and result processing

graph = graph_builder.compile()
