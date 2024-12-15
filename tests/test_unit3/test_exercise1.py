import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_3_1(student_submission):
    """Check that the student has implemented the checkpointing correctly."""
    try:
        graph = student_submission.graph
    except AttributeError:
        # Try to be slightly more robust in case the student forgets to name it 'graph'
        graph = student_submission
    # For this exercise, the student doesn't need to provide any inputs
    # (we will inject them ourselves)
    inputs = {}
    for step in graph.stream(inputs, return_all=True, stream_mode="debug"):
        for name, state in step.items():
            logger.debug(f"Checking step: {name}")
            if name == "chat_completion":
                if not state.get("messages"):
                    logging.debug("First time, no messages")
                    assert state["version"] == "v1"
                    assert state["metadata"] == {"last_restored": True}
                else:
                    logging.debug("Second time, should have messages now")
                    assert state["messages"] == []
                    assert state["version"] == "v1"
                    assert state["metadata"] == {"last_restored": False}
            elif name == "cleanup":
                if state["metadata"].get("last_restored"):
                    assert state["metadata"] == {
                        "last_restored": True,
                        "old_states_cleaned_up": False,
                    }
                else:
                    assert state["metadata"] == {"old_states_cleaned_up": True}
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
