import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_4_2(student_submission):
    """Check that the student has implemented the state editor correctly."""
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
            if name == "edit_handler":
                if not state.get("edits"):
                    logging.debug("First time, no edits")
                    assert state["edits"] == [
                        {"field": "message", "new_value": "Hello world!"}
                    ]
                    assert state["validators"] == {"message": lambda x: len(x) <= 20}
                    assert state["history"] == []
                else:
                    logging.debug("Second time, should have edits now")
                    assert state["edits"] == [
                        {"field": "message", "new_value": "Hello world!"}
                    ]
                    assert state["validators"] == {"message": lambda x: len(x) <= 20}
                    assert len(state["history"]) == 1
                    assert state["history"][0]["messages"][0].content == "Hello world!"
            elif name == "validation_logic":
                assert state["messages"][0].content == "Hello world!"
                assert state["edits"] == [
                    {"field": "message", "new_value": "Hello world!"}
                ]
                assert state["validators"] == {"message": lambda x: len(x) <= 20}
                assert len(state["history"]) == 1
                assert state["history"][0]["messages"][0].content == "Hello world!"
            elif name == "history_tracker":
                assert state["messages"][0].content == "Hello world!"
                assert state["edits"] == [
                    {"field": "message", "new_value": "Hello world!"}
                ]
                assert state["validators"] == {"message": lambda x: len(x) <= 20}
                assert len(state["history"]) == 2
                assert state["history"][0]["messages"][0].content == "Hello world!"
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
