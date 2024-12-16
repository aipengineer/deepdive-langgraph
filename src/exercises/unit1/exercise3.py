"""
Unit 1: Graph Basics & State Management
Exercise 1.3 - "Conditional Router"

Objective:
Create a graph that can classify incoming messages and route them to appropriate response
handlers based on the message content.

Requirements:
1. Message Classification:
   - Implement a classifier node that categorizes messages into at least 3 types
   - Include confidence scores for classifications
   - Maintain message history while adding classifications

2. Response Generation:
   - Create separate nodes for different types of responses
   - Each response node should generate an appropriate message
   - Maintain classification metadata in responses

3. Routing Logic:
   - Implement conditional routing based on message classification
   - Handle at least 3 different response paths
   - Ensure proper message and state flow through the graph

4. Expected Behavior:
   - "hello" type messages should get a greeting response
   - "help" type messages should get a help response
   - Unknown messages should get a fallback response
   - Each response should maintain proper message history

Graph Flow:
START -> classifier -> appropriate_response -> END
"""

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    State definition for the conversation router.

    Attributes:
        messages: List of conversation messages that accumulates using add_messages
        classification: Type of message determined by classifier
        confidence: Confidence score for the classification
    """

    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float


def classifier_node(state: State) -> State:
    """
    Classify incoming messages to determine appropriate response path.

    Args:
        state: Current state with messages to classify

    Returns:
        State with added classification and confidence

    Example:
        Input message "hello" should be classified as "greeting" with high confidence
    """
    # TODO: Implement message classification
    # 1. Get the last message from state
    # 2. Classify it based on content
    # 3. Return state with classification and confidence
    pass


def response_node_1(state: State) -> State:
    """Handle greeting responses."""
    # TODO: Implement greeting response
    # Return appropriate message while maintaining state
    pass


def response_node_2(state: State) -> State:
    """Handle help requests."""
    # TODO: Implement help response
    # Return appropriate message while maintaining state
    pass


def response_node_3(state: State) -> State:
    """Handle unknown messages."""
    # TODO: Implement fallback response
    # Return appropriate message while maintaining state
    pass


def get_next_node(state: State) -> str:
    """
    Determine the next node based on message classification.

    Args:
        state: Current state with classification

    Returns:
        Name of the next node to route to
    """
    # TODO: Implement routing logic
    # Return appropriate response node name based on classification
    pass


# Initialize the graph
graph_builder = StateGraph(State)

# TODO: Add your nodes
# Hint: You need classifier and response nodes

# TODO: Add your edges
# Hint: Consider the flow:
# 1. START to classifier
# 2. Classifier to response nodes (conditional)
# 3. Response nodes to END

# TODO: Compile the graph
graph = None  # Replace with proper compilation

# Default input for testing
default_input = {"messages": [], "classification": "", "confidence": 0.0}

# Make variables available for testing
__all__ = ["default_input", "graph"]
