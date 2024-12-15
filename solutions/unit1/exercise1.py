# UNIT 1: Graph Basics & State Management

# Exercise 1.1 - "Hello LangGraph"
# Requirements:
# - Create a StateGraph with a single LLM node
# - Define a basic State type using TypedDict and Annotated
# - Implement proper input/output message handling
# - Include basic error handling for API failures

from typing import Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def llm_node(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for the LLM node
    if not state.get("messages"):
        return {"messages": [HumanMessage(content="Hello!")]}
    else:
        last_message = state["messages"][-1]
        if last_message.content == "Hello!":
            return {"messages": [HumanMessage(content="How are you?")]}
        elif last_message.content == "How are you?":
            return {"messages": [HumanMessage(content="Goodbye!")]}
    return state


# Initialize the graph
graph_builder = StateGraph(State)

# Add the node
graph_builder.add_node("llm", llm_node)

# Add the edges
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", "llm")

graph = graph_builder.compile()
