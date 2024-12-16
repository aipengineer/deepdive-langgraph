"""
UNIT 2: Building Agents with LangGraph
Exercise 2.2 - "Multi-Tool Agent" - Updated with all required exports
"""

import logging
import math
import os
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
from langgraph.prebuilt import ToolNode
from langgraph.graph.state import CompiledStateGraph

from src.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set API keys in environment
os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Initialize models and tools
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tavily_tool = TavilySearchResults(tavily_api_key=settings.tavily_api_key)

class State(TypedDict, total=False):
    """State for the multi-tool agent with optional fields."""
    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]
    tool_usage: dict[str, int]
    rate_limits: dict[str, int]
    extracted_location: NotRequired[str | None]
    tool_name: NotRequired[str | None]
    tool_outputs: NotRequired[list[str]]


def extract_information_with_llm(message: str, instructions: str) -> str:
    """Extract information from a message using LLM."""
    logger.debug(f"Extracting information from: {message}")
    prompt = ChatPromptTemplate.from_messages([
        ("system", instructions),
        ("user", "{query}"),
    ])
    chain = prompt | llm
    response = chain.invoke({"query": message})
    extracted_info = response.content.strip()
    logger.debug(f"Extracted information: {extracted_info}")
    return extracted_info


@tool
def calculator(expression: str) -> str:
    """Calculate expression using Python's numexpr library."""
    logger.debug(f"Calculator received: {expression}")
    local_dict = {"pi": math.pi, "e": math.e}
    try:
        result = numexpr.evaluate(
            expression.strip(),
            global_dict={},
            local_dict=local_dict,
        )
        return str(float(result))
    except Exception as e:
        logger.error(f"Calculator error: {e}")
        return f"Error evaluating expression: {e}"


@tool
def check_weather(location: str, at_time: datetime | None = None) -> str:
    """Return the weather forecast for the specified location."""
    logger.debug(f"Weather check for: {location}")
    loc = location.strip()
    time_str = f" at {at_time}" if at_time else ""
    return f"It's always sunny in {loc}{time_str}"


def tool_selector(state: State) -> State:
    """Select appropriate tool based on message content and usage limits."""
    logger.debug("Entering tool_selector")

    # Initialize state on first call
    if not state.get("available_tools"):
        tools = [calculator, check_weather, tavily_tool]
        return {
            "messages": [HumanMessage(content="How can I help you today?")],
            "available_tools": tools,
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
            "extracted_location": None,
            "tool_name": None,
            "tool_outputs": [],
        }

    if not state.get("messages"):
        return state

    message = state["messages"][-1].content.lower()
    result_state = dict(state)

    def check_rate_limit(tool_name: str) -> bool:
        usage = state["tool_usage"].get(tool_name, 0)
        limit = state["rate_limits"].get(tool_name, float("inf"))
        return usage < limit

    if "weather" in message:
        if not check_rate_limit("check_weather"):
            return {
                **state,
                "messages": [
                    AIMessage(content="Rate limit exceeded for weather checks.")
                ],
                "tool_name": None,
            }
        location = extract_information_with_llm(
            message,
            "Extract the location from the weather query. Return only the location name.",
        )
        result_state.update({
            "tool_name": "check_weather",
            "extracted_location": location,
            "tool_usage": {
                **state["tool_usage"],
                "check_weather": state["tool_usage"].get("check_weather", 0) + 1,
            },
        })
    elif any(word in message for word in ["calculate", "compute", "solve", "+", "-", "*", "/"]):
        if not check_rate_limit("calculator"):
            return {
                **state,
                "messages": [
                    AIMessage(content="Rate limit exceeded for calculations.")
                ],
                "tool_name": None,
            }
        result_state.update({
            "tool_name": "calculator",
            "tool_usage": {
                **state["tool_usage"],
                "calculator": state["tool_usage"].get("calculator", 0) + 1,
            },
        })
    else:
        if not check_rate_limit("TavilySearchResults"):
            return {
                **state,
                "messages": [
                    AIMessage(content="Rate limit exceeded for searches.")
                ],
                "tool_name": None,
            }
        result_state.update({
            "tool_name": "TavilySearchResults",
            "tool_usage": {
                **state["tool_usage"],
                "TavilySearchResults": state["tool_usage"].get("TavilySearchResults", 0) + 1,
            },
        })

    return result_state


def _execute_direct_tool(state: State, tool_name: str, message: str, tool: Any) -> str:
    """Execute a tool directly (used mainly in testing contexts)."""
    logger.debug(f"Executing direct tool: {tool_name}")

    if tool_name == "calculator":
        expr = extract_information_with_llm(
            message,
            "Extract the mathematical expression. Return only the expression.",
        )
        output = tool(expr)
    else:  # check_weather
        location = state.get("extracted_location")
        if not location:
            location = extract_information_with_llm(
                message,
                "Extract the location from the weather query. Return only the location name.",
            )
        output = tool(location)

    logger.debug(f"Direct tool output: {output}")
    return output


def _execute_with_tool_node(state: State, tool_name: str, message: str, tools: list[Any]) -> dict:
    """Execute a tool using ToolNode."""
    logger.debug(f"Executing with ToolNode: {tool_name}")
    tool_node = ToolNode(tools)

    if tool_name == "calculator":
        expr = extract_information_with_llm(
            message,
            "Extract the mathematical expression. Return only the expression.",
        )
        return tool_node.invoke({
            "messages": [
                AIMessage(content="",
                          tool_code=[{"name": "calculator", "expression": expr}])
            ]
        })
    elif tool_name == "check_weather":
        location = state.get("extracted_location")
        if not location:
            location = extract_information_with_llm(
                message,
                "Extract the location from the weather query. Return only the location name.",
            )
        return tool_node.invoke({
            "messages": [
                AIMessage(content="",
                          tool_code=[{"name": "check_weather", "location": location}])
            ]
        })
    else:  # TavilySearchResults
        return tool_node.invoke({
            "messages": [
                AIMessage(content=message,
                          tool_code=[{"name": "TavilySearchResults", "query": message}])
            ]
        })


def _process_tool_output(result: Any) -> str:
    """Process the output from a tool execution."""
    if isinstance(result, dict) and "messages" in result and result["messages"]:
        return result["messages"][0].content
    return str(result)


def tool_executor(state: State) -> State:
    """Execute the selected tool with appropriate parameters."""
    logger.debug(f"Executing tool: {state.get('tool_name')}")

    if not state.get("tool_name"):
        return {**state, "tool_outputs": []}

    try:
        tool_name = state["tool_name"]
        message = state["messages"][-1].content
        tools = state.get("available_tools", [])

        # Handle direct tool execution for testing
        if len(tools) == 1 and tool_name in ["calculator", "check_weather"]:
            output = _execute_direct_tool(state, tool_name, message, tools[0])
        else:
            # Handle normal flow with ToolNode
            result = _execute_with_tool_node(state, tool_name, message, tools)
            output = _process_tool_output(result)

        logger.debug(f"Final tool output: {output}")
        return {**state, "tool_outputs": [output]}

    except Exception as e:
        logger.exception("Tool execution error")
        return {**state, "tool_outputs": [f"Error: {str(e)}"]}


def result_processor(state: State) -> State:
    """Process tool execution results."""
    logger.debug("Processing results")
    if not state.get("tool_outputs"):
        return state

    tool_output = state["tool_outputs"][-1]
    return {
        **state,
        "messages": state.get("messages", []) + [AIMessage(content=str(tool_output))]
    }


def get_next_step(state: State) -> Literal["tool_selector", "end"]:
    """Determine the next step in the conversation."""
    logger.debug("Checking next step")

    if not state.get("messages"):
        logger.debug("No messages, returning end")
        return "end"

    last_message = state["messages"][-1]

    # End conditions
    if isinstance(last_message, HumanMessage):
        if "thanks" in last_message.content.lower():
            logger.debug("Thanks detected, ending conversation")
            return "end"
        if "bye" in last_message.content.lower():
            logger.debug("Goodbye detected, ending conversation")
            return "end"

    # Also end if we've completed a tool execution
    if isinstance(last_message, AIMessage) and state.get("tool_outputs"):
        logger.debug("Tool execution complete, ending cycle")
        return "end"

    logger.debug("Continuing to tool selection")
    return "tool_selector"


def create_agent() -> CompiledStateGraph:
    """Create and configure the agent graph.

    Returns:
        CompiledStateGraph: The compiled agent graph ready for execution.
    """
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("tool_selector", tool_selector)
    graph.add_node("tool_executor", tool_executor)
    graph.add_node("result_processor", result_processor)

    # Add edges
    graph.add_edge(START, "tool_selector")
    graph.add_edge("tool_selector", "tool_executor")
    graph.add_edge("tool_executor", "result_processor")

    # Add conditional edges for ending the conversation
    graph.add_conditional_edges(
        "result_processor",  # Move conditional edge to result_processor
        get_next_step,
        {
            "tool_selector": "tool_selector",
            "end": END,
        }
    )

    return graph.compile()


# Make sure we pass all required state fields in the default input
default_input = {
    "messages": [],
    "available_tools": [],
    "tool_usage": {},
    "rate_limits": {},
    "tool_name": None,
    "tool_outputs": [],
}
# Create the graph
graph = create_agent()

# Update exports
__all__ = [
    "calculator",
    "check_weather",
    "extract_information_with_llm",
    "tool_executor",
    "tool_selector",
    "result_processor",
    "get_next_step",
    "graph",
    "default_input",  # Added default_input to exports
]