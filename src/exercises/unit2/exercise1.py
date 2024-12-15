"""
# UNIT 2: Building Agents with LangGraph

Exercise 2.2 - "Multi-Tool Agent"

Your task is to build a multi-tool agent that can handle different
types of queries by selecting and using appropriate tools.
The agent should be able to:
1. Use a search tool (TavilySearchResults) for general queries
2. Perform mathematical calculations using a calculator tool
3. Provide weather information using a weather checking tool
4. Manage tool usage with rate limits

Requirements:
- Integrate multiple tools (search, calculator, weather)
- Implement tool selection logic based on message content
- Add tool usage constraints (rate limits, usage quotas)
- Include tool usage explanations to users
- Handle errors gracefully

Tips:
- Use the @tool decorator to create new tools
- Consider keywords in messages to select appropriate tools
- Implement proper rate limiting and usage tracking
- Make sure to handle edge cases and errors
"""

from datetime import datetime
from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

from src.config import settings


# First, implement these tool definitions
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expression using Python's numexpr library.

    TODO: Implement this tool to:
    1. Use numexpr to safely evaluate mathematical expressions
    2. Handle basic arithmetic and mathematical functions
    3. Include proper error handling
    """
    pass  # Your implementation here


@tool
def check_weather(location: str, at_time: datetime | None = None) -> str:
    """Return the weather forecast for the specified location.

    TODO: Implement this tool to:
    1. Accept a location parameter
    2. Optionally accept a time parameter
    3. Return a weather forecast string
    """
    pass  # Your implementation here


class State(TypedDict):
    """State for the multi-tool agent."""

    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]
    tool_usage: dict[str, int]
    rate_limits: dict[str, Any]


def tool_selector(state: State) -> State:
    """Select appropriate tool based on the message content and usage limits.

    TODO: Implement this function to:
    1. Initialize tools and usage tracking on first call
    2. Select appropriate tool based on message content
    3. Track tool usage and enforce rate limits
    4. Return tool_name or rate limit exceeded message
    """
    pass  # Your implementation here


def llm_node(state: State) -> State:
    """Process messages with LLM and tool binding.

    TODO: Implement this function to:
    1. Handle initial state with no messages
    2. Process different types of queries
    3. Maintain conversation flow
    4. Return appropriate responses
    """
    pass  # Your implementation here


def tool_executor(state: State) -> State:
    """Execute the selected tool with appropriate parameters.

    TODO: Implement this function to:
    1. Extract tool name and parameters from state
    2. Execute the appropriate tool with correct parameters
    3. Handle tool execution errors
    4. Return tool outputs in the correct format
    """
    pass  # Your implementation here


def result_processor(state: State) -> State:
    """Process tool execution results.

    TODO: Implement this function to:
    1. Extract tool output from state
    2. Format the output appropriately
    3. Return the processed result as a message
    """
    pass  # Your implementation here


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("tool_selector", tool_selector)
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_executor", tool_executor)
graph_builder.add_node("result_processor", result_processor)

# TODO: Add the edges to connect the nodes
# 1. Connect START to tool_selector
# 2. Connect tool_selector to llm
# 3. Connect llm back to tool_selector when there are messages
# 4. Connect tool_selector to tool_executor when there's a tool_name
# 5. Connect tool_executor to result_processor
# 6. Connect result_processor back to llm

graph_builder.add_edge(START, "tool_selector")
# Add your remaining edge implementations here

# Compile the graph
graph = graph_builder.compile()
