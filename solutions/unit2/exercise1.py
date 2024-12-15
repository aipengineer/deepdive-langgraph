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
from typing import Annotated, Any, TypedDict
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages

from src.config import settings


class State(TypedDict):
    """
State
for our simple tool user."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


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
    else:
        return {"messages": [HumanMessage(content="Thanks for the information!")]}


def tool_executor(state: State) -> State:
    """Execute the selected tool."""
    if not state.get("tool_calls"):
        return {
            "tool_outputs": []  # Ensure we always return tool_outputs
        }

    tool_call = state["tool_calls"][-1]
    if tool_call["tool_name"] == "TavilySearchResults":
        # Initialize tool with API key from settings
        tool = TavilySearchResults(tavily_api_key=settings.tavily_api_key)
        try:
            output = tool.invoke({"query": tool_call["args"]["query"]})
            return {"tool_outputs": [json.dumps(output)]}
        except Exception as e:
            return {"tool_outputs": [json.dumps({"error": str(e)})]}

    return {
        "tool_outputs": []
    }


def result_processor(state: State) -> State:
    """Process tool execution results."""
    if not state.get("tool_outputs"):
        return {
            "messages": [],
            "tool_calls": [],
            "tool_outputs": []
        }

    tool_output = state["tool_outputs"][-1]
    return {
        "messages": [HumanMessage(content=str(tool_output))],
        "tool_calls": [],
        "tool_outputs": [],
    }


def create_agent() -> StateGraph:
    """Create and configure the agent graph."""
    # Initialize graph
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("llm", llm_node)
    graph.add_node("tool_executor", tool_executor)
    graph.add_node("result_processor", result_processor)

    # Add edges
    graph.add_edge(START, "llm")
    graph.add_edge("llm", "tool_executor")
    graph.add_edge("tool_executor", "result_processor")
    graph.add_edge("result_processor", "llm")

    # Set entry point
    graph.set_entry_point("llm")

    return graph.compile()

# Create the graph
graph = create_agent()