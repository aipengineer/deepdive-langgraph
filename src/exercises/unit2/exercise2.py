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
"""

from datetime import datetime
from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph


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


def get_next_step(state: State) -> Literal["tool_selector", "end"]:
    """Determine the next step in the conversation.

    Args:
        state: The current state of the conversation

    Returns:
        Literal["tool_selector", "end"]: The next step to take
    """
    if not state.get("messages"):
        return "end"
    last_message = state["messages"][-1]
    if (
        isinstance(last_message, HumanMessage)
        and "thanks" in last_message.content.lower()
    ):
        return "end"
    return "tool_selector"


def tool_selector(state: State) -> State | None:
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
def create_agent() -> CompiledStateGraph:
    """Create and configure the agent graph.

    Returns:
        CompiledStateGraph: The compiled graph ready for execution
    """
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
