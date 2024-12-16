"""
UNIT 1: Graph Basics & State Management

Exercise 1.2 - "Message Memory"
Extension of Exercise 1.1 with message history management
"""

from datetime import datetime
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int


def llm_response(state: State) -> State:
    """Generate responses based on conversation history."""
    if not state.get("messages"):
        return {
            "messages": [
                HumanMessage(
                    content="Hello!",
                    metadata={"timestamp": datetime.now().isoformat(), "role": "user"},
                )
            ],
            "summary": "",
            "window_size": 3,
        }

    last_message = state["messages"][-1]
    response_map = {
        "Hello!": "How are you?",
        "How are you?": "Goodbye!"
    }

    if last_message.content in response_map:
        return {
            "messages": [
                HumanMessage(
                    content=response_map[last_message.content],
                    metadata={"timestamp": datetime.now().isoformat(), "role": "assistant"},
                )
            ],
            "summary": state["summary"],
            "window_size": state["window_size"],
        }

    return state


def message_windowing(state: State) -> State:
    """Maintain a sliding window of recent messages."""
    if len(state["messages"]) > state["window_size"]:
        state["messages"] = state["messages"][-state["window_size"]:]
    return state


def summary_generation(state: State) -> State:
    """Generate a summary when conversation gets long enough."""
    if len(state["messages"]) > 2:
        messages_text = " -> ".join([m.content for m in state["messages"]])
        state["summary"] = f"Conversation summary: {messages_text}"
    return state


def should_end(state: State) -> bool:
    """Determine if we should end the conversation."""
    if not state["messages"]:
        return False
    return state["messages"][-1].content == "Goodbye!"


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes for different conversation processing stages
graph_builder.add_node("llm_response", llm_response)
graph_builder.add_node("message_windowing", message_windowing)
graph_builder.add_node("summary_generation", summary_generation)

# Add edges to create the processing pipeline
graph_builder.add_edge(START, "llm_response")
graph_builder.add_edge("llm_response", "message_windowing")
graph_builder.add_edge("message_windowing", "summary_generation")

# Add conditional edges based on conversation state
graph_builder.add_conditional_edges(
    "summary_generation",
    should_end,
    {
        True: END,
        False: "llm_response"
    }
)

# Compile the graph
graph = graph_builder.compile()

# Define default input
default_input = {"messages": [], "summary": "", "window_size": 3}

# Make variables available for testing
__all__ = ["graph", "default_input"]