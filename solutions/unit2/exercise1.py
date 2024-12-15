# UNIT 2: Building Agents with LangGraph

# Exercise 2.1 - "Simple Tool User"
# Requirements:
# - Create a graph that integrates with TavilySearchResults tool
# - Implement proper tool calling with JSON validation
# - Add retry logic for failed tool calls
# - Include proper error messaging to users

from typing import Annotated, Any, TypedDict

from langchain.tools import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


def llm_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for the LLM node with tool binding
    if not state.get("messages"):
        return {
            "messages": [HumanMessage(content="What is the capital of France?")],
            "tool_calls": [],
            "tool_outputs": [],
        }
    elif state["messages"][-1].content == "What is the capital of France?":
        return {
            "tool_calls": [
                {
                    "tool_name": "TavilySearchResults",
                    "args": {"query": "capital of France"},
                }
            ]
        }
    else:
        return {"messages": [HumanMessage(content="Thanks for the information!")]}
    return state


def tool_executor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for executing the tool
    tool_call = state["tool_calls"][-1]
    if tool_call["tool_name"] == "TavilySearchResults":
        tool = TavilySearchResults()
        try:
            output = tool.run(tool_call["args"]["query"])
            return {"tool_outputs": [output]}
        except Exception as e:
            return {"tool_outputs": [f"Error: {e}"]}
    return state


def result_processor(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for processing tool results
    tool_output = state["tool_outputs"][-1]
    return {"messages": [HumanMessage(content=tool_output)]}


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_executor", tool_executor)
graph_builder.add_node("result_processor", result_processor)

# Add the edges
graph_builder.add_edge(START, "llm")
graph_builder.add_edge(
    "llm", "tool_executor", condition=lambda state: state.get("tool_calls")
)
graph_builder.add_edge("tool_executor", "result_processor")
graph_builder.add_edge("result_processor", "llm")

graph = graph_builder.compile()
