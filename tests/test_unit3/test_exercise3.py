import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_3_3(student_submission):
    """Check that the student has implemented the thread management correctly."""
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
            if name == "manage_thread_pool":
                if not state.get("thread_id"):
                    logging.debug("First time, no thread id")
                    assert state["thread_id"] == "thread_1"
                    assert state["shared_data"] == {"counter": 0}
                    assert state["locks"] == []
                elif state["thread_id"] == "thread_1":
                    logging.debug("Second time, thread 1")
                    assert state["thread_id"] == "thread_2"
                    assert state["shared_data"] == {"counter": 1}
                    assert state["locks"] == []
                else:
                    logging.debug("Third time, thread 2")
                    assert state["thread_id"] is None
                    assert state["shared_data"] == {"counter": 3, "status": "healthy"}
                    assert state["locks"] == []
            elif name == "synchronize_data":
                if state["thread_id"] == "thread_1":
                    assert state["shared_data"] == {"counter": 2}
                    assert state["locks"] == ["counter"]
                elif state["thread_id"] == "thread_2":
                    assert state["shared_data"] == {"counter": 3}
                    assert state["locks"] == ["counter"]
                else:
                    raise ValueError(f"Unknown thread id: {state['thread_id']}")
            elif name == "monitor_threads":
                assert state["shared_data"] == {"counter": 3, "status": "healthy"}
                assert state["locks"] == []
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
