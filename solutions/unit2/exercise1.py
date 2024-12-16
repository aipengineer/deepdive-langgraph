"""
UNIT 2: Building Agents with LangGraph
Exercise 2.1 - "Simple Tool User"

Requirements:
- Create a graph that integrates with TavilySearchResults tool
- Implement proper tool calling with JSON validation
- Add retry logic for failed tool calls
- Include proper error messaging to users
"""

import json
import os
from typing import Annotated, Any, TypedDict

from langchain_community.tools import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from src.config import settings

# Set Tavily API key in environment
os.environ["TAVILY_API_KEY"] = settings.tavily_api_key

# Initialize tool once at module level
tavily_tool = TavilySearchResults()


class State(TypedDict):
    """State for our simple tool user."""

    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


def should_end(state: State) -> bool:
    """Determine if we should end the conversation."""
    if not state.get("messages"):
        return False

    last_message = state["messages"][-1].content
    return "Thanks for the information!" in last_message


def llm_node(state: State) -> State:
    """Process messages and determine tool usage."""
    # Handle initial state
    if not state.get("messages"):
        return {
            "messages": [HumanMessage(content="What is the capital of France?")],
            "tool_calls": [],
            "tool_outputs": [],
        }

    # Handle existing message
    last_message = state["messages"][-1].content
    if "capital of France" in last_message:
        return {
            "tool_calls": [
                {
                    "tool_name": "TavilySearchResults",
                    "args": {"query": "capital of France"},
                }
            ]
        }

    return {
        "messages": [HumanMessage(content="Thanks for the information!")],
        "tool_calls": [],
        "tool_outputs": [],
    }


def tool_executor(state: State) -> State:
    """Execute the selected tool."""
    if not state.get("tool_calls"):
        return {"tool_outputs": []}

    tool_call = state["tool_calls"][-1]
    if tool_call["tool_name"] == "TavilySearchResults":
        try:
            output = tavily_tool.invoke(tool_call["args"])
            return {"tool_outputs": [json.dumps(output)]}
        except Exception as e:
            return {"tool_outputs": [json.dumps({"error": str(e)})]}

    return {"tool_outputs": []}


def result_processor(state: State) -> State:
    """Process tool execution results."""
    if not state.get("tool_outputs"):
        return {"messages": [], "tool_calls": [], "tool_outputs": []}

    tool_output = state["tool_outputs"][-1]
    return {
        "messages": [HumanMessage(content=str(tool_output))],
        "tool_calls": [],
        "tool_outputs": [],
    }


# Initialize the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_executor", tool_executor)
graph_builder.add_node("result_processor", result_processor)

# Add edges
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", "tool_executor")
graph_builder.add_edge("tool_executor", "result_processor")

# Add conditional edges to either continue or end
graph_builder.add_conditional_edges(
    "result_processor", should_end, {True: END, False: "llm"}
)

# Compile the graph
graph = graph_builder.compile()

# Define default input with all required state fields
default_input = {"messages": [], "tool_calls": [], "tool_outputs": []}

# Make variables available for testing
__all__ = ["default_input", "graph"]
