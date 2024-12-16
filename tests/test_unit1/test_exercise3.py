import logging
from typing import Any

from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)


def verify_response(
    state: dict[str, Any],
    input_text: str,
    expected_response: str,
    expected_classification: str,
    min_confidence: float,
) -> None:
    """Helper function to verify responses."""
    # Check message accumulation
    assert (
        len(state["messages"]) == 2
    ), f"Expected 2 messages, got {len(state['messages'])}"

    # Check message contents
    assert state["messages"][0].content == input_text
    assert state["messages"][1].content == expected_response

    # Check classification and confidence
    assert state["classification"] == expected_classification
    assert state["confidence"] >= min_confidence


def test_exercise_1_3(student_submission):
    """Check that the student has implemented the conditional router correctly."""
    try:
        graph = student_submission.graph
        default_input = student_submission.default_input
    except AttributeError:
        graph = student_submission
        default_input = {"messages": [], "classification": "", "confidence": 0.0}

    # Test case 1: Greeting
    state = graph.invoke({**default_input, "messages": [HumanMessage(content="Hello")]})
    verify_response(
        state=state,
        input_text="Hello",
        expected_response="Hello there!",
        expected_classification="greeting",
        min_confidence=0.8,
    )

    # Test case 2: Help request
    state = graph.invoke(
        {**default_input, "messages": [HumanMessage(content="I need help")]}
    )
    verify_response(
        state=state,
        input_text="I need help",
        expected_response="How can I help you?",
        expected_classification="help",
        min_confidence=0.7,
    )

    # Test case 3: Unknown input
    state = graph.invoke(
        {**default_input, "messages": [HumanMessage(content="Foo bar")]}
    )
    verify_response(
        state=state,
        input_text="Foo bar",
        expected_response="I don't understand.",
        expected_classification="unknown",
        min_confidence=0.0,  # Unknown messages have low confidence
    )

    logger.info("All routing tests passed successfully!")
