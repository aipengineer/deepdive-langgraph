"""
UNIT 2: Building Agents with LangGraph
Exercise 2.3 - "Parallel Tool Executor with Fan-out/Fan-in"
"""

import asyncio
import json
import logging
import os
from typing import Annotated, Any, TypedDict, cast

from langchain_community.tools import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from src.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set up tools
os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
tavily_tool = TavilySearchResults()

class State(TypedDict):
    """State for parallel tool executor with reducer."""
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict]
    results: dict[str, Any]
    errors: dict[str, str]

def create_default_state() -> State:
    """Create a default state with all required fields."""
    return {
        "messages": [HumanMessage(content="Starting parallel tool execution...")],
        "pending_tools": [
            {
                "id": "search_1",
                "tool_name": "TavilySearchResults",
                "args": {"query": "capital of France"},
            },
            {
                "id": "search_2",
                "tool_name": "TavilySearchResults",
                "args": {"query": "largest city in Japan"},
            },
        ],
        "results": {},
        "errors": {},
    }

def ensure_valid_state(state: dict) -> State:
    """Ensure state has all required fields with valid values."""
    logger.debug(f"Ensuring valid state for input: {state}")

    default_state = create_default_state()

    # If state is empty or None, return default state
    if not state:
        logger.debug("Empty state detected, using default state")
        return default_state

    # Ensure all required fields exist with valid values
    valid_state = {
        "messages": state.get("messages", default_state["messages"]),
        "pending_tools": state.get("pending_tools", default_state["pending_tools"]),
        "results": state.get("results", default_state["results"]),
        "errors": state.get("errors", default_state["errors"]),
    }

    # Ensure messages is never empty
    if not valid_state["messages"]:
        valid_state["messages"] = default_state["messages"]

    logger.debug(f"Validated state: {valid_state}")
    return cast(State, valid_state)

def init_state(state: dict) -> State:
    """Initialize state and create tool tasks."""
    logger.debug(f"Initializing state with input: {state}")

    # Ensure valid state
    valid_state = ensure_valid_state(state)
    logger.debug(f"State after initialization: {valid_state}")

    return valid_state

async def execute_tool(tool_call: dict) -> tuple[str, Any]:
    """Execute a single tool call asynchronously."""
    logger.debug(f"Executing tool: {tool_call}")
    try:
        result = await asyncio.to_thread(
            tavily_tool.invoke,
            tool_call["args"]
        )
        logger.debug(f"Tool execution successful: {result}")
        return tool_call["id"], result
    except Exception as e:
        logger.error(f"Tool execution failed: {str(e)}")
        return tool_call["id"], f"Error: {str(e)}"

async def parallel_executor(state: dict) -> State:
    """Execute multiple tools in parallel with fan-out."""
    logger.debug(f"Starting parallel execution with state: {state}")

    # Ensure valid state
    current_state = ensure_valid_state(state)

    # If no pending tools, return current state
    if not current_state["pending_tools"]:
        logger.debug("No pending tools found")
        return current_state

    # Execute pending tools in parallel
    logger.debug(f"Executing {len(current_state['pending_tools'])} tools in parallel")
    tasks = [execute_tool(tool_call) for tool_call in current_state["pending_tools"]]
    results = await asyncio.gather(*tasks)

    # Process results
    new_results = {}
    new_errors = {}

    for tool_id, result in results:
        if isinstance(result, str) and result.startswith("Error:"):
            logger.error(f"Tool {tool_id} failed: {result}")
            new_errors[tool_id] = result
        else:
            logger.debug(f"Tool {tool_id} succeeded")
            new_results[tool_id] = result

    final_state = {
        "messages": current_state["messages"],
        "pending_tools": [],  # Clear pending tools after execution
        "results": new_results,
        "errors": new_errors
    }

    logger.debug(f"Parallel execution completed. Final state: {final_state}")
    return cast(State, final_state)

def result_aggregator(state: dict) -> State:
    """Aggregate results from parallel execution with fan-in."""
    logger.debug(f"Aggregating results from state: {state}")

    # Ensure valid state
    current_state = ensure_valid_state(state)
    messages = list(current_state["messages"])

    # Process successful results
    for tool_id, result in current_state["results"].items():
        logger.debug(f"Processing result from {tool_id}")
        messages.append(
            HumanMessage(content=f"Result from {tool_id}: {json.dumps(result, ensure_ascii=False)}")
        )

    final_state = {
        "messages": messages,
        "pending_tools": [],
        "results": current_state["results"],
        "errors": current_state["errors"]
    }

    logger.debug(f"Results aggregated. Final state: {final_state}")
    return cast(State, final_state)

def error_handler(state: dict) -> State:
    """Handle errors from parallel execution."""
    logger.debug(f"Handling errors from state: {state}")

    # Ensure valid state
    current_state = ensure_valid_state(state)
    messages = list(current_state["messages"])

    # Process errors
    for tool_id, error in current_state["errors"].items():
        logger.debug(f"Processing error from {tool_id}")
        messages.append(
            HumanMessage(content=f"Error from {tool_id}: {error}")
        )

    final_state = {
        "messages": messages,
        "pending_tools": [],
        "results": current_state["results"],
        "errors": current_state["errors"]
    }

    logger.debug(f"Errors handled. Final state: {final_state}")
    return cast(State, final_state)

def route_results(state: dict) -> str:
    """Route to appropriate handler based on state."""
    logger.debug(f"Routing based on state: {state}")

    # Ensure valid state
    current_state = ensure_valid_state(state)

    if current_state.get("errors"):
        logger.debug("Routing to error_handler")
        return "error_handler"

    logger.debug("Routing to result_aggregator")
    return "result_aggregator"

# Initialize the graph
logger.info("Initializing graph")
graph = StateGraph(State)

# Add nodes
logger.debug("Adding nodes to graph")
graph.add_node("init", init_state)
graph.add_node("parallel_executor", parallel_executor)
graph.add_node("result_aggregator", result_aggregator)
graph.add_node("error_handler", error_handler)

# Add edges
logger.debug("Adding edges to graph")
graph.add_edge(START, "init")
graph.add_edge("init", "parallel_executor")

# Add conditional routing
graph.add_conditional_edges(
    "parallel_executor",
    route_results,
    {
        "result_aggregator": "result_aggregator",
        "error_handler": "error_handler"
    }
)

graph.add_edge("result_aggregator", END)
graph.add_edge("error_handler", END)

# Compile graph
logger.info("Compiling graph")
graph = graph.compile()

# Default input state
default_input = create_default_state()

# Make variables available for testing
__all__ = ["graph", "default_input"]