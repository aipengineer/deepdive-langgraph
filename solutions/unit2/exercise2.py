"""
UNIT 2: Building Agents with LangGraph
Solution for Exercise 2.2 - "Multi-Tool Agent"

This solution implements a multi-tool agent that can:
1. Handle different types of queries using appropriate tools
2. Track and limit tool usage
3. Process results and maintain conversation flow
"""

import math
from datetime import datetime
from typing import Annotated, Any, Literal, TypedDict

import numexpr
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph


@tool
def calculator(expression: str) -> str:
    """Calculate expression using Python's numexpr library."""
    local_dict = {"pi": math.pi, "e": math.e}
    try:
        result = numexpr.evaluate(
            expression.strip(),
            global_dict={},  # restrict access to globals
            local_dict=local_dict,  # add common mathematical functions
        )
        return str(float(result))
    except Exception as e:
        return f"Error evaluating expression: {e!s}"


@tool
def check_weather(location: str, at_time: datetime | None = None) -> str:
    """Return the weather forecast for the specified location."""
    loc = location.strip()
    time_str = f" at {at_time}" if at_time else ""
    return f"It's always sunny in {loc}{time_str}"


class State(TypedDict):
    """State for the multi-tool agent."""

    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]
    tool_usage: dict[str, int]
    rate_limits: dict[str, Any]


def get_next_step(state: State) -> Literal["tool_selector", "end"]:
    """Determine the next step in the conversation."""
    if not state.get("messages"):
        return "end"
    last_message = state["messages"][-1]
    if (
        isinstance(last_message, HumanMessage)
        and "thanks" in last_message.content.lower()
    ):
        return "end"
    return "tool_selector"


def tool_selector(state: State) -> State:
    """Select appropriate tool based on message content and usage limits."""
    # Initialize tools and usage tracking on first call
    if not state.get("available_tools"):
        return {
            "messages": [],
            "available_tools": [
                TavilySearchResults(),
                calculator,
                check_weather,
            ],
            "tool_usage": {
                "TavilySearchResults": 0,
                "calculator": 0,
                "check_weather": 0,
            },
            "rate_limits": {
                "TavilySearchResults": 2,
                "calculator": 3,
                "check_weather": 1,
            },
        }

    # Select tool based on message content
    if state.get("messages"):
        message = state["messages"][-1].content.lower()

        # Determine appropriate tool
        if "weather" in message:
            tool_name = "check_weather"
        elif any(
            word in message
            for word in ["calculate", "compute", "solve", "+", "-", "*", "/"]
        ):
            tool_name = "calculator"
        else:
            tool_name = "TavilySearchResults"

        # Check rate limits
        if state["tool_usage"][tool_name] < state["rate_limits"][tool_name]:
            state["tool_usage"][tool_name] += 1
            return {"tool_name": tool_name}
        else:
            return {
                "messages": [
                    HumanMessage(
                        content=f"Rate limit exceeded for {tool_name}. "
                        f"Please try a different query."
                    )
                ]
            }
    return state


def llm_node(state: State) -> State:
    """Process messages with LLM and tool binding."""
    # Handle initial or empty state
    if not state.get("messages"):
        return {
            "messages": [HumanMessage(content="How can I help you today?")],
        }

    # Process the last message and prepare response
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        if "thanks" in last_message.content.lower():
            return {
                "messages": [
                    HumanMessage(
                        content="You're welcome! Let me know if you need anything else."
                    )
                ]
            }
        return state
    return state


def tool_executor(state: State) -> State:
    """Execute the selected tool with appropriate parameters."""
    tool_name = state["tool_name"]
    message = state["messages"][-1].content

    try:
        if tool_name == "check_weather":
            # Extract location from message
            location = message.lower().replace("weather", "").replace("in", "").strip()
            output = check_weather(location=location)
        elif tool_name == "calculator":
            # Extract mathematical expression
            expr = (
                message.lower()
                .replace("calculate", "")
                .replace("compute", "")
                .replace("solve", "")
                .strip()
            )
            output = calculator(expression=expr)
        else:
            # Use TavilySearchResults for general queries
            tool = next(
                tool
                for tool in state["available_tools"]
                if isinstance(tool, TavilySearchResults)
            )
            output = tool.invoke({"query": message})

        return {"tool_outputs": [output]}
    except Exception as e:
        return {"tool_outputs": [f"Error executing {tool_name}: {e!s}"]}


def result_processor(state: State) -> State:
    """Process tool execution results."""
    tool_output = state["tool_outputs"][-1]
    return {"messages": [HumanMessage(content=str(tool_output))]}


def create_agent() -> CompiledStateGraph:
    """Create and configure the agent graph."""
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("tool_selector", tool_selector)
    graph.add_node("llm", llm_node)
    graph.add_node("tool_executor", tool_executor)
    graph.add_node("result_processor", result_processor)

    # Add basic edges
    graph.add_edge(START, "tool_selector")
    graph.add_edge("tool_selector", "llm")
    graph.add_edge("tool_selector", "tool_executor")
    graph.add_edge("tool_executor", "result_processor")
    graph.add_edge("result_processor", "llm")

    # Add conditional edge from llm to either continue or end
    graph.add_conditional_edges(
        source="llm",
        path=get_next_step,
        path_map={
            "tool_selector": "tool_selector",
            "end": END,
        },
    )

    # Set entry point
    graph.set_entry_point("tool_selector")

    return graph.compile()


# Create the graph
graph = create_agent()
