# UNIT 2: Building Agents with LangGraph

# Exercise 2.3 - "Parallel Tool Executor"
# Requirements:
# - Implement parallel tool execution
# - Add result aggregation logic
# - Implement proper error handling for partial failures
# - Include progress reporting

import asyncio
from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict]
    results: dict[str, Any]
    errors: dict[str, str]


async def execute_tool(tool_call: dict) -> tuple[str, Any]:
    """Helper function to execute a single tool asynchronously."""
    tool_name = tool_call["tool_name"]
    tool = globals()[tool_name]()  # Instantiate the tool
    try:
        if tool_name == "WeatherSearchTool":
            result = await asyncio.to_thread(tool.run, tool_call["args"]["query"])
        else:
            result = await asyncio.to_thread(tool.run, tool_call["args"])
        return tool_name, result
    except Exception as e:
        return tool_name, f"Error: {e}"


async def parallel_executor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for parallel tool execution
    if not state.get("pending_tools"):
        return {
            "messages": [],
            "pending_tools": [
                {
                    "tool_name": "TavilySearchResults",
                    "args": {"query": "capital of France"},
                },
                {"tool_name": "LLMMathChain", "args": "2 + 2"},
                {
                    "tool_name": "WeatherSearchTool",
                    "args": {"query": "weather in London"},
                },
            ],
            "results": {},
            "errors": {},
        }
    else:
        tasks = [execute_tool(tool_call) for tool_call in state["pending_tools"]]
        results = await asyncio.gather(*tasks)
        for tool_name, result in results:
            if "Error:" in result:
                state["errors"][tool_name] = result
            else:
                state["results"][tool_name] = result
        return state


def result_aggregator(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for aggregating tool results
    for tool_name, result in state["results"].items():
        state["messages"].append(HumanMessage(content=f"{tool_name}: {result}"))
    return state


def error_handler(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for handling tool errors
    for tool_name, error in state["errors"].items():
        state["messages"].append(
            HumanMessage(content=f"Error with {tool_name}: {error}")
        )
    return state


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("parallel_executor", parallel_executor)
graph_builder.add_node("result_aggregator", result_aggregator)
graph_builder.add_node("error_handler", error_handler)

# Add the edges
graph_builder.add_edge(START, "parallel_executor")
graph_builder.add_edge("parallel_executor", "result_aggregator")
graph_builder.add_edge(
    "parallel_executor", "error_handler", condition=lambda state: state["errors"]
)

graph = graph_builder.compile()
