"""
# UNIT 2: Building Agents with LangGraph
Exercise 2.1 - "Simple Tool User"

Your task is to create a simple conversational agent that uses the Tavily search tool
to answer questions. The agent should:

1. Start by asking "What is the capital of France?"
2. Use the TavilySearchResults tool to search for the answer
3. Return the search results
4. End with a "Thanks for the information!" message

Requirements:
- Create a graph that integrates with TavilySearchResults tool
- Implement proper tool calling with JSON validation
- Add retry logic for failed tool calls
- Include proper error messaging to users
- Properly end the conversation after the search is complete

Tips:
- Use the TavilySearchResults tool from langchain_community.tools
- Make sure to set up proper state management
- Follow the conversation flow: question -> search -> response -> thanks
- Remember to handle tool execution errors gracefully
- Use conditional edges to end the conversation properly
"""

import os
from typing import Annotated, Any, TypedDict

from langchain_community.tools import TavilySearchResults
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
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
    """Determine if we should end the conversation.

    TODO: Implement this function to:
    1. Handle empty state case
    2. Check the last message content
    3. Return True if the message is "Thanks for the information!"
    4. Return False otherwise
    """
    pass  # Your implementation here


def llm_node(state: State) -> State:
    """Process messages and determine tool usage.

    TODO: Implement this function to:
    1. Handle initial empty state by returning:
       - Initial question about France's capital
       - Empty tool_calls and tool_outputs lists
    2. When asked about France's capital:
       - Return a tool call for TavilySearchResults
       - Include proper search query in the args
    3. In other cases:
       - Return a thank you message
       - Clear tool calls and outputs
    """
    pass  # Your implementation here


def tool_executor(state: State) -> State:
    """Execute the selected tool.

    TODO: Implement this function to:
    1. Handle case with no tool calls
    2. Execute TavilySearchResults tool with proper args
    3. Convert tool output to JSON string
    4. Handle any execution errors properly
    """
    pass  # Your implementation here


def result_processor(state: State) -> State:
    """Process tool execution results.

    TODO: Implement this function to:
    1. Handle case with no tool outputs
    2. Process the tool output
    3. Return output as a message
    4. Clear tool calls and outputs
    """
    pass  # Your implementation here


# Initialize the graph
graph_builder = StateGraph(State)

# TODO: Add the nodes to the graph
# 1. Add llm_node
# 2. Add tool_executor
# 3. Add result_processor

# TODO: Add the edges to connect the nodes
# 1. Connect START to llm
# 2. Connect llm to tool_executor
# 3. Connect tool_executor to result_processor
# 4. Add conditional edges from result_processor using should_end
#    - If True: go to END
#    - If False: go back to llm

# After implementing the TODOs above:
# 1. Compile the graph
graph = graph_builder.compile()

# 2. Define default input
default_input = {"messages": [], "tool_calls": [], "tool_outputs": []}

# 3. Make variables available for testing
__all__ = ["default_input", "graph"]
