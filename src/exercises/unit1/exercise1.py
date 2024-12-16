"""
Unit 1: Graph Basics & State Management
Exercise 1.1 - "Hello LangGraph"

Objective:
Create a simple conversational graph that follows a fixed pattern:
1. Start with "Hello!"
2. Respond with "How are you?"
3. End with "Goodbye!"

Requirements:
1. State Management:
   - Use TypedDict to define a State type with a messages field
   - Use Annotated and add_messages for proper message handling

2. Node Implementation:
   - Create a single LLM node that manages the conversation flow
   - Handle the empty initial state case
   - Process each message to determine the next response
   - Return appropriate state updates

3. Graph Structure:
   - Initialize a StateGraph with the proper State type
   - Add the LLM node and necessary edges
   - Implement proper conversation ending condition
   - Use START and END appropriately

4. Expected Behavior:
   - Should support a 3-message conversation
   - Must properly terminate after "Goodbye!"
   - Should handle the initial empty state
"""

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    Defines the state structure for our conversation graph.

    Attributes:
        messages: A list of messages in the conversation.
                 Uses add_messages as a reducer to combine message lists.
    """
    messages: Annotated[list[BaseMessage], add_messages]


def llm_node(state: State) -> State:
    """
    Processes the current state and returns the next message in the conversation.

    Args:
        state: Current conversation state containing the message history

    Returns:
        Updated state with the next message added

    The node should:
    1. Handle empty initial state
    2. Process the last message to determine the next response
    3. Return state updates with the new message
    """
    # TODO: Implement the conversation logic
    pass


def should_end(state: State) -> bool:
    """
    Determines if the conversation should end.

    Args:
        state: Current conversation state

    Returns:
        True if the conversation should end, False otherwise
    """
    # TODO: Implement the ending condition
    pass


# Initialize the graph
graph_builder = StateGraph(State)

# Add the node
graph_builder.add_node("llm", llm_node)

# TODO: Add the edges
# Hint: You'll need:
# 1. A starting edge
# 2. Conditional edges to either continue or end the conversation

# TODO: Compile the graph
graph = None  # Replace with proper compilation

# Default input for testing
default_input = {"messages": []}

# Make variables available for testing
__all__ = ["graph", "default_input"]