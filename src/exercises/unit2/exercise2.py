"""
# UNIT 2: Building Agents with LangGraph

Exercise 2.2 - "Multi-Tool Agent"

In this exercise, you'll build a multi-tool agent that can intelligently select and use
different tools based on user queries. The agent should:

1. Support multiple tools:
   - Calculator for mathematical expressions
   - Weather checker for location-based weather queries
   - Search tool (TavilySearchResults) for general queries

2. Implement tool selection and execution:
   - Select appropriate tool based on message content
   - Extract relevant information using LLMs
   - Execute tools with proper parameters

3. Handle tool usage limits:
   - Track usage of each tool
   - Enforce rate limits
   - Provide appropriate feedback when limits are exceeded

4. Manage conversation flow:
   - Process tool outputs
   - Handle errors gracefully
   - End conversations appropriately

Requirements:
- Use LangGraph's StateGraph for orchestration
- Implement proper LLM-based information extraction
- Handle all tools through both direct execution and ToolNode
- Maintain conversation state including tool usage history
"""

import logging
import math
from datetime import datetime
from typing import Annotated, Any, Literal, NotRequired, TypedDict

import numexpr
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from src.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize models and tools
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tavily_tool = TavilySearchResults(tavily_api_key=settings.tavily_api_key)

class State(TypedDict, total=False):
    """State for the multi-tool agent.

    Implement this TypedDict to include:
    - Message history
    - Available tools
    - Tool usage tracking
    - Rate limits
    - Tool execution context (extracted info, selected tool, outputs)
    """
    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]
    tool_usage: dict[str, int]
    rate_limits: dict[str, int]
    extracted_location: NotRequired[str | None]
    tool_name: NotRequired[str | None]
    tool_outputs: NotRequired[list[str]]


def extract_information_with_llm(message: str, instructions: str) -> str:
    """Extract information from a message using LLM.

    TODO: Implement this function to:
    1. Create a prompt that extracts specific information based on instructions
    2. Use the LLM to process the message
    3. Return the extracted information
    """
    pass  # Your implementation here


@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expression using Python's numexpr library.

    TODO: Implement this function to:
    1. Safely evaluate mathematical expressions
    2. Handle basic arithmetic and mathematical functions
    3. Include proper error handling
    """
    pass  # Your implementation here


@tool
def check_weather(location: str, at_time: datetime | None = None) -> str:
    """Return the weather forecast for the specified location.

    TODO: Implement this function to:
    1. Process the location parameter
    2. Handle optional time parameter
    3. Return a weather forecast string
    """
    pass  # Your implementation here


def tool_selector(state: State) -> State:
    """Select appropriate tool based on message content and usage limits.

    TODO: Implement this function to:
    1. Initialize tools and usage tracking on first call
    2. Select appropriate tool based on message content
    3. Track tool usage and enforce rate limits
    4. Extract necessary information (e.g., location for weather)
    """
    pass  # Your implementation here


def tool_executor(state: State) -> State:
    """Execute the selected tool with appropriate parameters.

    TODO: Implement this function to:
    1. Handle both direct tool execution and ToolNode-based execution
    2. Extract required information using LLM
    3. Process tool outputs
    4. Handle errors appropriately
    """
    pass  # Your implementation here


def result_processor(state: State) -> State:
    """Process tool execution results.

    TODO: Implement this function to:
    1. Handle tool outputs
    2. Format responses
    3. Update conversation state
    """
    pass  # Your implementation here


def get_next_step(state: State) -> Literal["tool_selector", "end"]:
    """Determine the next step in the conversation.

    TODO: Implement this function to:
    1. Check conversation state
    2. Identify end conditions
    3. Determine when to continue tool selection
    """
    pass  # Your implementation here


def create_agent() -> CompiledStateGraph:
    """Create and configure the agent graph.

    TODO: Implement this function to:
    1. Create StateGraph instance
    2. Add all required nodes
    3. Configure edges and conditional routing
    4. Handle conversation end conditions
    """
    pass  # Your implementation here


# Default input for testing
default_input = {
    "messages": [],
    "available_tools": [],
    "tool_usage": {},
    "rate_limits": {},
    "tool_name": None,
    "tool_outputs": [],
}

# Create the graph (implement create_agent first)
graph = None  # Will be created by create_agent()

# Make components available for testing
__all__ = [
    "calculator",
    "check_weather",
    "extract_information_with_llm",
    "tool_executor",
    "tool_selector",
    "result_processor",
    "get_next_step",
    "graph",
    "default_input",
]