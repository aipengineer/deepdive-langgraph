import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_3_2(student_submission):
    """Check that the student has implemented the branching correctly."""
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
            if name == "create_branch":
                if not state.get("branch_id"):
                    logging.debug("First time, no branch id")
                    assert state["branch_id"] == "branch_1"
                    assert state["parent_checkpoint"] == "main"
                    assert state["changes"] == []
                elif state["branch_id"] == "branch_1":
                    logging.debug("Second time, branch 1")
                    assert state["branch_id"] == "branch_2"
                    assert state["parent_checkpoint"] == "main"
                    assert state["changes"] == []
                else:
                    logging.debug("Third time, branch 2")
                    assert state["branch_id"] == "main"
                    assert state["parent_checkpoint"] is None
                    assert state["changes"] == [
                        {"message": "This is a change from branch 1"},
                        {"message": "This is a change from branch 2"},
                    ]
            elif name == "diff_states":
                if state["branch_id"] == "branch_1":
                    assert state["changes"] == [
                        {"message": "This is a change from branch 1"}
                    ]
                elif state["branch_id"] == "branch_2":
                    assert state["changes"] == [
                        {"message": "This is a change from branch 2"}
                    ]
                else:
                    raise ValueError(f"Unknown branch id: {state['branch_id']}")
            elif name == "merge_branches":
                assert state["branch_id"] == "main"
                assert state["parent_checkpoint"] is None
                assert state["changes"] == [
                    {"message": "This is a change from branch 1"},
                    {"message": "This is a change from branch 2"},
                ]
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
