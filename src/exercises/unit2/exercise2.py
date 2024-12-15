# UNIT 2: Building Agents with LangGraph

# Exercise 2.2 - "Multi-Tool Agent"
# Requirements:
# - Integrate multiple tools (search, math, weather)
# - Implement tool selection logic
# - Add tool usage constraints (rate limits, usage quotas)
# - Include tool usage explanations to users

from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]
    tool_usage: dict[str, int]
    rate_limits: dict[str, Any]


def tool_selector(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for selecting the appropriate tool


def llm_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for the LLM node with tool binding


def tool_executor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for executing the selected tool


def result_processor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for processing tool results


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("tool_selector", tool_selector)
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_executor", tool_executor)
graph_builder.add_node("result_processor", result_processor)

# Add the edges
graph_builder.add_edge(START, "tool_selector")
# You must implement the edges for LLM node, tool execution, and result processing

graph = graph_builder.compile()
