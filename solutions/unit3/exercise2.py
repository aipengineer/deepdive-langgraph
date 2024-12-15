# UNIT 3: Checkpointing & Persistence

# Exercise 3.2 - "Time Travel"
# Requirements:
# - Implement checkpoint branching
# - Add state diffing functionality
# - Implement branch merging
# - Add branch cleanup logic

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    branch_id: str
    parent_checkpoint: str
    changes: list[dict]


def create_branch(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for creating a new branch
    if not state.get("branch_id"):
        return {
            "messages": [],
            "branch_id": "branch_1",
            "parent_checkpoint": "main",
            "changes": [],
        }
    elif state["branch_id"] == "branch_1":
        return {
            "messages": [],
            "branch_id": "branch_2",
            "parent_checkpoint": "main",
            "changes": [],
        }
    return state


def diff_states(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for diffing two states
    if state["branch_id"] == "branch_1":
        return {"changes": [{"message": "This is a change from branch 1"}]}
    elif state["branch_id"] == "branch_2":
        return {"changes": [{"message": "This is a change from branch 2"}]}
    return state


def merge_branches(state: State) -> State:
    """This is a stub, you should implement this yourself."""
    # Implement the logic for merging two branches
    return {
        "messages": [],
        "branch_id": "main",
        "parent_checkpoint": None,
        "changes": [
            {"message": "This is a change from branch 1"},
            {"message": "This is a change from branch 2"},
        ],
    }


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
graph_builder.add_edge("merge_branches", "create_branch")

graph = graph_builder.compile()
