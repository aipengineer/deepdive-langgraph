"""
Unit 1: Graph Basics & State Management
Exercise 1.2 - "Message Memory"

Objective:
Extend Exercise 1.1 to create a more sophisticated conversation manager that:
1. Maintains a sliding window of recent messages
2. Generates summaries of longer conversations
3. Includes metadata with messages
4. Follows the same conversation flow (Hello -> How are you? -> Goodbye)

Requirements:
1. State Management:
   - Extend the State type to include summary and window_size
   - Track message metadata (timestamps, roles)
   - Maintain conversation history with sliding window

2. Node Implementation:
   - llm_response: Generate appropriate responses with metadata
   - message_windowing: Implement sliding window logic
   - summary_generation: Create summaries for longer conversations
   - should_end: Determine when to end the conversation

3. Graph Structure:
   - Create a pipeline of nodes for message processing
   - Implement proper conversation ending condition
   - Connect nodes in the correct order
"""

from datetime import datetime
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    Extended state for message memory management.

    Attributes:
        messages: List of conversation messages with metadata
        summary: Current conversation summary
        window_size: Maximum number of messages to keep
    """
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int


def llm_response(state: State) -> State:
    """
    Generate responses while maintaining conversation context.

    Args:
        state: Current conversation state with message history

    Returns:
        Updated state with new message and preserved context

    Notes:
        - Handle empty initial state
        - Add appropriate metadata to messages
        - Follow the Hello -> How are you? -> Goodbye flow
    """
    # TODO: Implement response generation with metadata
    pass


def message_windowing(state: State) -> State:
    """
    Maintain a sliding window of recent messages.

    Args:
        state: Current conversation state

    Returns:
        State with message history trimmed to window size
    """
    # TODO: Implement sliding window logic
    pass


def summary_generation(state: State) -> State:
    """
    Generate summaries for longer conversations.

    Args:
        state: Current conversation state

    Returns:
        State with updated summary if needed
    """
    # TODO: Implement summary generation
    pass


def should_end(state: State) -> bool:
    """
    Determine if the conversation should end.

    Args:
        state: Current conversation state

    Returns:
        True if the conversation should end, False otherwise
    """
    # TODO: Implement ending condition
    pass


# Initialize the graph
graph_builder = StateGraph(State)

# TODO: Add your nodes
# Hint: You need llm_response, message_windowing, and summary_generation

# TODO: Add your edges
# Hint: Consider the order of operations:
# 1. Generate response
# 2. Apply windowing
# 3. Update summary
# 4. Decide whether to continue or end

# TODO: Compile the graph
graph = None  # Replace with proper compilation

# Default input for testing
default_input = {"messages": [], "summary": "", "window_size": 3}

# Make variables available for testing
__all__ = ["graph", "default_input"]