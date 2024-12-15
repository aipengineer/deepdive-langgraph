# UNIT 3: Checkpointing & Persistence

# Exercise 3.3 - "Multi-Thread Management"
# Requirements:
# - Implement thread pooling
# - Add thread synchronization
# - Implement thread cleanup
# - Add thread monitoring

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    thread_id: str
    shared_data: dict[str, Any]
    locks: list[str]


def manage_thread_pool(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for managing the thread pool
    if not state.get("thread_id"):
        return {
            "messages": [],
            "thread_id": "thread_1",
            "shared_data": {"counter": 0},
            "locks": [],
        }
    elif state["thread_id"] == "thread_1":
        return {
            "messages": [],
            "thread_id": "thread_2",
            "shared_data": {"counter": 1},
            "locks": [],
        }
    return state


def synchronize_data(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for synchronizing shared data
    if state["thread_id"] == "thread_1":
        state["shared_data"]["counter"] += 1
        return {"locks": ["counter"]}
    elif state["thread_id"] == "thread_2":
        state["shared_data"]["counter"] += 2
        return {"locks": ["counter"]}
    return state


def monitor_threads(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for monitoring thread health
    return {"shared_data": {"counter": 3, "status": "healthy"}}


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("manage_thread_pool", manage_thread_pool)
graph_builder.add_node("synchronize_data", synchronize_data)
graph_builder.add_node("monitor_threads", monitor_threads)

# Add the edges
graph_builder.add_edge(START, "manage_thread_pool")
graph_builder.add_edge("manage_thread_pool", "synchronize_data")
graph_builder.add_edge("synchronize_data", "monitor_threads")
graph_builder.add_edge("monitor_threads", "manage_thread_pool")

graph = graph_builder.compile()
