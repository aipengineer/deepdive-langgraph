# UNIT 1: Graph Basics & State Management

# Exercise 1.2 - "Message Memory"
# Requirements:
# - Extend Exercise 1.1 to maintain conversation context
# - Add a message summarization node for long conversations
# - Implement a configurable message window size
# - Add metadata to messages (timestamps, roles, etc.)

from datetime import datetime
from typing import Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int


def llm_response(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for generating LLM responses
    if not state.get("messages"):
        return {
            "messages": [
                HumanMessage(
                    content="Hello!",
                    metadata={"timestamp": datetime.now(), "role": "user"},
                )
            ],
            "summary": "",
            "window_size": 3,
        }
    else:
        last_message = state["messages"][-1]
        if last_message.content == "Hello!":
            return {
                "messages": [
                    HumanMessage(
                        content="How are you?",
                        metadata={"timestamp": datetime.now(), "role": "user"},
                    )
                ]
            }
        elif last_message.content == "How are you?":
            return {
                "messages": [
                    HumanMessage(
                        content="Goodbye!",
                        metadata={"timestamp": datetime.now(), "role": "user"},
                    )
                ]
            }
    return state


def message_windowing(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for managing message window
    state["messages"] = state["messages"][-state["window_size"] :]
    return state


def summary_generation(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for generating conversation summaries
    if len(state["messages"]) > 2:
        state["summary"] = "Conversation summary: ..."
    return state


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("llm_response", llm_response)
graph_builder.add_node("message_windowing", message_windowing)
graph_builder.add_node("summary_generation", summary_generation)

# Add the edges
graph_builder.add_edge(START, "llm_response")
graph_builder.add_edge("llm_response", "message_windowing")
graph_builder.add_edge("message_windowing", "summary_generation")
graph_builder.add_edge("summary_generation", "llm_response")

graph = graph_builder.compile()
