# UNIT 3: Checkpointing & Persistence

# Exercise 3.2 - "Time Travel"
# Requirements:
# - Implement checkpoint branching
# - Add state diffing functionality
# - Implement branch merging
# - Add branch cleanup logic

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    branch_id: str
    parent_checkpoint: str
    changes: list[dict]


def create_branch(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for creating a new branch


def diff_states(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for diffing two states


def merge_branches(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    pass  # Implement the logic for merging two branches


# Initialize the graph
graph_builder = StateGraph(State)

# Add the nodes
graph_builder.add_node("create_branch", create_branch)
graph_builder.add_node("diff_states", diff_states)
graph_builder.add_node("merge_branches", merge_branches)

# Add the edges
graph_builder.add_edge(START, "create_branch")
graph_builder.add_edge("create_branch", "diff_states")
graph_builder.add_edge("diff_states", "merge_branches")

graph = graph_builder.compile()
