# UNIT 2: Building Agents with LangGraph

# Exercise 2.2 - "Multi-Tool Agent"
# Requirements:
# - Integrate multiple tools (search, math, weather)
# - Implement tool selection logic
# - Add tool usage constraints (rate limits, usage quotas)
# - Include tool usage explanations to users

from typing import Annotated, Any

from langchain.tools import (
    LLMMathChain,
    TavilySearchResults,
    WeatherSearchTool,
)
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]
    tool_usage: dict[str, int]
    rate_limits: dict[str, Any]


def tool_selector(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for selecting the appropriate tool
    if not state.get("available_tools"):
        return {
            "messages": [],
            "available_tools": [
                TavilySearchResults(),
                LLMMathChain(),
                WeatherSearchTool(),
            ],
            "tool_usage": {
                "TavilySearchResults": 0,
                "LLMMathChain": 0,
                "WeatherSearchTool": 0,
            },
            "rate_limits": {
                "TavilySearchResults": 2,
                "LLMMathChain": 3,
                "WeatherSearchTool": 1,
            },
        }
    else:
        message = state["messages"][-1].content
        if "weather" in message.lower():
            tool_name = "WeatherSearchTool"
        elif any(
            keyword in message.lower() for keyword in ["calculate", "compute", "solve"]
        ):
            tool_name = "LLMMathChain"
        else:
            tool_name = "TavilySearchResults"

        if state["tool_usage"][tool_name] < state["rate_limits"][tool_name]:
            state["tool_usage"][tool_name] += 1
            return {"tool_name": tool_name}
        else:
            return {
                "messages": [
                    HumanMessage(content=f"Rate limit exceeded for {tool_name}")
                ]
            }
    return state


def llm_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for the LLM node with tool binding
    if not state.get("messages"):
        return {
            "messages": [HumanMessage(content="What is the weather in London today?")],
        }
    elif state["messages"][-1].content == "What is the weather in London today?":
        return {"messages": [HumanMessage(content="Calculate 2 + 2")]}
    elif state["messages"][-1].content == "Calculate 2 + 2":
        return {"messages": [HumanMessage(content="What is the capital of France?")]}
    else:
        return {"messages": [HumanMessage(content="Thanks for the information!")]}
    return state


def tool_executor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for executing the selected tool
    tool_name = state["tool_name"]
    tool = next(
        tool for tool in state["available_tools"] if type(tool).__name__ == tool_name
    )
    message = state["messages"][-1].content
    try:
        if tool_name == "WeatherSearchTool":
            output = tool.run(message)
        elif tool_name == "LLMMathChain":
            output = tool.run(message)
        else:
            output = tool.run({"query": message})
        return {"tool_outputs": [output]}
    except Exception as e:
        return {"tool_outputs": [f"Error: {e}"]}


def result_processor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for processing tool results
    tool_output = state["tool_outputs"][-1]
    return {"messages": [HumanMessage(content=tool_output)]}


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("tool_selector", tool_selector)
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_executor", tool_executor)
graph_builder.add_node("result_processor", result_processor)

# Add the edges
graph_builder.add_edge(START, "tool_selector")
graph_builder.add_edge("tool_selector", "llm")
graph_builder.add_edge(
    "llm", "tool_selector", condition=lambda state: state.get("messages")
)
graph_builder.add_edge(
    "tool_selector", "tool_executor", condition=lambda state: state.get("tool_name")
)
graph_builder.add_edge("tool_executor", "result_processor")
graph_builder.add_edge("result_processor", "llm")

graph = graph_builder.compile()
