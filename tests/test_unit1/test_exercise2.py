import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def test_exercise_1_2(student_submission):
    """Check that the student has implemented the message memory correctly."""
    try:
        graph = student_submission.graph
        default_input = student_submission.default_input
    except AttributeError:
        # Try to be slightly more robust in case the student forgets to name it 'graph'
        graph = student_submission
        default_input = {"messages": [], "summary": "", "window_size": 3}

    # Use the provided default input
    final_output = graph.invoke(default_input)

    # Verify the final state
    assert "messages" in final_output
    assert "summary" in final_output
    assert "window_size" in final_output

    messages = final_output["messages"]
    assert len(messages) == 3, "Expected exactly 3 messages in the conversation"

    # Check the conversation flow
    expected_sequence = ["Hello!", "How are you?", "Goodbye!"]
    for msg, expected_content in zip(messages, expected_sequence, strict=False):
        assert msg.content == expected_content

        # Check metadata
        assert "timestamp" in msg.metadata
        assert "role" in msg.metadata
        # Verify timestamp is in ISO format and parseable
        try:
            datetime.fromisoformat(msg.metadata["timestamp"])
        except ValueError:
            raise AssertionError("Timestamp should be in ISO format")

        # Verify proper role assignment
        assert msg.metadata["role"] in ["user", "assistant"]

    # Verify window size enforcement
    assert len(messages) <= final_output["window_size"]

    # Verify summary generation
    if len(messages) > 2:
        assert final_output["summary"].startswith("Conversation summary:")
        # Verify all messages are included in summary
        for msg in messages:
            assert msg.content in final_output["summary"]
    else:
        assert final_output["summary"] == ""

    logger.info("All checks passed successfully!")
