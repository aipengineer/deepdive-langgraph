import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_1_2(student_submission):
    """Check that the student has implemented the message memory correctly."""
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
            if name == "llm_response":
                if not state.get("messages"):
                    logging.debug("First time, no messages")
                    assert len(state["messages"]) == 1
                    assert state["messages"][0].content == "Hello!"
                    assert state["summary"] == ""
                    assert state["window_size"] == 3
                else:
                    logging.debug("Second time, should have messages now")
                    assert len(state["messages"]) == 1
                    if state["messages"][0].content == "Hello!":
                        assert state["messages"][0].content == "How are you?"
                    elif state["messages"][0].content == "How are you?":
                        assert state["messages"][0].content == "Goodbye!"
                    else:
                        assert False, "Unexpected message content"
            elif name == "message_windowing":
                assert len(state["messages"]) <= state["window_size"]
            elif name == "summary_generation":
                if len(state["messages"]) > 2:
                    assert state["summary"] == "Conversation summary: ..."
                else:
                    assert state["summary"] == ""
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
