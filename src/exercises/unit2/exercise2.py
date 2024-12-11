from typing import Annotated, Optional, Dict, List

from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list, add_messages]
    available_tools: List[ToolNode]
    tool_usage: Dict[str, int]
    rate_limits: Dict[str, int]  # Rate limit per tool (calls per conversation)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4")

# Build the graph
graph_builder = StateGraph(State)

def llm_node(state: State) -> State:
    """
    This node is executed whenever the graph is invoked.
    It takes the current graph state, calls an LLM, and returns a new state.
    This includes deciding which tool to use (if any) and updating the tool_code.
    """
    messages = state["messages"]
    tool_code = state.get("tool_code")  # Tool code from previous step (if any)

    # TODO: Implement LLM call logic here
    # - Use the last message in the state as the prompt
    # - Include tool_code (if available) to continue multi-tool sequences
    # - If a tool is suggested by the LLM, update tool_code in the returned state
    # - Handle LLM API errors gracefully

    return {
        "messages": [AIMessage(content="I'm sorry, I don't understand.")],
        "tool_code": None,
    }

def tool_selection_node(state: State) -> State:
    """
    This node selects the appropriate tool based on the tool_code in the state.
    It also enforces rate limits and updates tool usage.
    """
    tool_code = state["tool_code"]
    available_tools = state["available_tools"]
    tool_usage = state["tool_usage"]
    rate_limits = state["rate_limits"]

    # TODO: Implement tool selection and rate limiting logic here
    # - Identify the correct tool based on tool_code
    # - Check if the tool's rate limit has been reached
    # - If rate limit is exceeded, return an appropriate message to the user
    # - If the tool can be used, update tool_usage and return the ToolMessage

    return {
        "messages": [
            AIMessage(content="I'm sorry, I can't use that tool right now.")
        ],
        "tool_code": None,
    }

# Define your tool functions here (search, math, weather)
# Each tool function should take in a State and return a State
# Ensure each tool function updates the "messages" key in the state with a ToolMessage
# containing the tool's output

# TODO: Implement at least three tool functions (search, math, weather)

# Add nodes to the graph
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_selection", tool_selection_node)
# TODO: Add nodes for your tool functions

# Add edges
graph_builder.add_edge(START, "llm")
graph_builder.add_conditional_edges("llm", tools_condition)
graph_builder.add_edge("tool_selection", "llm")  # Return to LLM after tool use

graph = graph_builder.compile()