# UNIT 1: Graph Basics & State Management

# Exercise 1.1 - "Hello LangGraph"
# Requirements:
# - Create a StateGraph with a single LLM node
# - Define a basic State type using TypedDict and Annotated
# - Implement proper input/output message handling
# - Include basic error handling for API failures

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def llm_node(state: State) -> State:
    """Process messages in a simple conversational flow."""
    # Get the last message to determine next response
    if not state["messages"]:
        return {"messages": [HumanMessage(content="Hello!")]}

    last_message = state["messages"][-1]

    # Simple conversation flow
    response_map = {
        "Hello!": "How are you?",
        "How are you?": "Goodbye!",
    }

    if last_message.content in response_map:
        return {"messages": [HumanMessage(content=response_map[last_message.content])]}

    return state


def should_end(state: State) -> bool:
    """Determine if we should end based on the last message."""
    if not state["messages"]:
        return False
    return state["messages"][-1].content == "Goodbye!"


# Initialize the graph
graph_builder = StateGraph(State)

# Add the node
graph_builder.add_node("llm", llm_node)

# Add the conditional edges
graph_builder.add_edge(START, "llm")
graph_builder.add_conditional_edges(
    "llm",
    should_end,
    {
        True: END,
        False: "llm"
    }
)

# Compile the graph
graph = graph_builder.compile()

# Define the default input
default_input = {"messages": []}

# Make sure both the graph and default_input are available when importing
__all__ = ["graph", "default_input"]