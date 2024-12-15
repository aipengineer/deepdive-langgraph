import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_4_1(student_submission):
    """Check that the student has implemented the approval flow correctly."""
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
            if name == "request_approval":
                if not state.get("pending_approvals"):
                    logging.debug("First time, no pending approvals")
                    assert state["pending_approvals"] == [
                        {"action": "send_email", "status": "pending"}
                    ]
                    assert state["approved_actions"] == []
                    assert state["notifications"] == []
                else:
                    logging.debug("Second time, should have pending approvals now")
                    assert state["pending_approvals"] == [
                        {"action": "send_email", "status": "approved"}
                    ]
                    assert state["approved_actions"] == [{"action": "send_email"}]
                    assert state["notifications"] == []
            elif name == "review_handler":
                assert state["pending_approvals"] == [
                    {"action": "send_email", "status": "approved"}
                ]
                assert state["approved_actions"] == [{"action": "send_email"}]
                assert state["notifications"] == []
            elif name == "notification_sender":
                assert state["pending_approvals"] == [
                    {"action": "send_email", "status": "approved"}
                ]
                assert state["approved_actions"] == [{"action": "send_email"}]
                assert state["notifications"] == ["Email sent successfully!"]
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
