"""
UNIT 2: Building Agents with LangGraph
Exercise 2.2 - "Multi-Tool Agent"

This solution implements a multi-tool agent that can:
1. Handle different types of queries using appropriate tools
2. Track and limit tool usage
3. Process results and maintain conversation flow
4. Use LLM for intelligent location extraction
"""

import logging
import math
import os
from datetime import datetime
from typing import Annotated, Any, Literal, TypedDict

import numexpr
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode  # Import ToolNode

from src.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set API keys in environment
os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Initialize tools and models
tavily_tool = TavilySearchResults(tavily_api_key=settings.tavily_api_key)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


class State(TypedDict):
    """State for the multi-tool agent."""

    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]
    tool_usage: dict[str, int]
    rate_limits: dict[str, int]
    extracted_location: str | None
    tool_name: str | None
    tool_outputs: list[str]


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


def extract_information_with_llm(message: str, instructions: str) -> str:
    """Extract information from a message using LLM."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                instructions,  # Pass instructions dynamically
            ),
            ("user", "{query}"),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"query": message})
    return response.content.strip()


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
    """Select appropriate tool based on message content and enforce rate limits."""
    # Initialize state on first call
    if not state.get("available_tools"):
        # Define tools list
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

    # Check rate limits before selecting tool
    def check_rate_limit(tool_name: str) -> bool:
        usage = state["tool_usage"].get(tool_name, 0)
        limit = state["rate_limits"].get(tool_name, float("inf"))
        return usage < limit

    # Determine tool and handle rate limits
    if "weather" in message:
        if not check_rate_limit("check_weather"):
            return {
                "messages": [
                    AIMessage(
                        content="Rate limit exceeded for weather checks. Please try again later."
                    )
                ],
                "tool_name": None,
            }
        location = extract_information_with_llm(
            message,
            "Extract the location from the weather query. Respond with only the location name.",
        )
        return {
            "tool_name": "check_weather",
            "extracted_location": location,
            "tool_usage": {
                **state["tool_usage"],
                "check_weather": state["tool_usage"].get("check_weather", 0) + 1,
            },
        }
    elif any(
        word in message
        for word in ["calculate", "compute", "solve", "+", "-", "*", "/"]
    ):
        if not check_rate_limit("calculator"):
            return {
                "messages": [
                    AIMessage(
                        content="Rate limit exceeded for calculations. Please try again later."
                    )
                ],
                "tool_name": None,
            }
        return {
            "tool_name": "calculator",
            "tool_usage": {
                **state["tool_usage"],
                "calculator": state["tool_usage"].get("calculator", 0) + 1,
            },
        }
    else:
        if not check_rate_limit("TavilySearchResults"):
            return {
                "messages": [
                    AIMessage(
                        content="Rate limit exceeded for searches. Please try again later."
                    )
                ],
                "tool_name": None,
            }
        return {
            "tool_name": "TavilySearchResults",
            "tool_usage": {
                **state["tool_usage"],
                "TavilySearchResults": state["tool_usage"].get("TavilySearchResults", 0)
                + 1,
            },
        }


def tool_executor(state: State) -> State:
    """Execute the selected tool with appropriate parameters."""
    if not state.get("tool_name"):
        logger.debug("No tool selected.")
        return {"tool_outputs": []}

    tool_name = state["tool_name"]
    message = state["messages"][-1].content
    available_tools = state.get("available_tools", [])
    logger.debug(f"Available tools: {available_tools}")

    # Initialize ToolNode here with available tools
    tool_node = ToolNode(available_tools)

    try:
        if tool_name == "check_weather":
            location = state.get("extracted_location")
            if not location:
                location = extract_information_with_llm(
                    message,
                    "Extract the location from the weather query. Respond with only the location name.",
                )
            output = tool_node.invoke(
                {
                    "messages": [
                        AIMessage(
                            content="",
                            tool_code=[{"name": "check_weather", "location": location}],
                        )
                    ]
                }
            )
        elif tool_name == "calculator":
            expr = extract_information_with_llm(
                message,
                "Extract the numerical expression from the message. Respond with only the expression.",
            )
            output = tool_node.invoke(
                {
                    "messages": [
                        AIMessage(
                            content="",
                            tool_code=[{"name": "calculator", "expression": expr}],
                        )
                    ]
                }
            )
        else:
            output = tool_node.invoke(
                {
                    "messages": [
                        AIMessage(
                            content=message,
                            tool_code=[
                                {"name": "TavilySearchResults", "query": message}
                            ],
                        )
                    ]
                }
            )

        if output["messages"]:
            output = output["messages"][0].content
        return {"tool_outputs": [str(output)]}

    except Exception as e:
        logger.exception(f"Error executing {tool_name}: {e!s}")
        return {"tool_outputs": [f"Error executing {tool_name}: {e!s}"]}


def result_processor(state: State) -> State:
    """Process tool execution results."""
    if not state.get("tool_outputs"):
        return {"messages": []}

    tool_output = state["tool_outputs"][-1]
    return {"messages": [AIMessage(content=str(tool_output))]}


def llm_node(state: State) -> State:
    """Process messages with LLM."""
    if not state.get("messages"):
        return {"messages": [AIMessage(content="How can I help you today?")]}

    last_message = state["messages"][-1]
    if (
        isinstance(last_message, HumanMessage)
        and "thanks" in last_message.content.lower()
    ):
        return {
            "messages": [
                AIMessage(
                    content="You're welcome! Let me know if you need anything else."
                )
            ]
        }

    return state


# Initialize the graph
graph = StateGraph(State)

# Add nodes
graph.add_node("llm", llm_node)
graph.add_node("tool_selector", tool_selector)
graph.add_node("tool_executor", tool_executor)
graph.add_node("result_processor", result_processor)

# Add edges
graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    get_next_step,
    {
        "tool_selector": "tool_selector",
        "end": END,
    },
)
graph.add_edge("tool_selector", "tool_executor")
graph.add_edge("tool_executor", "result_processor")
graph.add_edge("result_processor", END)

# Compile the graph
graph = graph.compile()

# Make variables available for testing
__all__ = ["calculator", "check_weather", "graph"]
