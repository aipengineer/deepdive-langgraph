import logging

# The logger is used to check that the nodes are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_1_1(student_submission):
    """Check that the student has implemented the basic graph correctly."""
    try:
        graph = student_submission.graph
        default_input = student_submission.default_input
    except AttributeError:
        # Try to be slightly more robust in case the student forgets to name it 'graph'
        graph = student_submission
        default_input = {"messages": []}

    # Use invoke with the default input
    final_output = graph.invoke(default_input)

    # Validate the conversation flow
    messages = final_output["messages"]
    assert len(messages) == 3, "Expected 3 messages in the conversation"

    # Check the conversation flow
    expected_sequence = ["Hello!", "How are you?", "Goodbye!"]
    for actual, expected in zip(messages, expected_sequence, strict=False):
        assert (
            actual.content == expected
        ), f"Expected '{expected}' but got '{actual.content}'"

    logger.info("Test passed successfully!")
