import json
import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_2_1(student_submission):
    """Check that the student has implemented the simple tool user correctly."""
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
            if name == "llm":
                if not state.get("messages"):
                    logging.debug("First time, no messages")
                    assert (
                        state["messages"][0].content == "What is the capital of France?"
                    )
                    assert state["tool_calls"] == []
                    assert state["tool_outputs"] == []
                elif state["messages"][-1].content == "What is the capital of France?":
                    logging.debug("Second time, should have a tool call")
                    assert state["tool_calls"][0] == {
                        "tool_name": "TavilySearchResults",
                        "args": {"query": "capital of France"},
                    }
                else:
                    logging.debug("Third time, should have a thank you message")
                    assert (
                        state["messages"][-1].content == "Thanks for the information!"
                    )
            elif name == "tool_executor":
                logging.debug("Checking tool executor")
                # Check that the tool output is valid JSON
                try:
                    json.loads(state["tool_outputs"][0])
                except json.JSONDecodeError:
                    assert False, "Tool output is not valid JSON"
            elif name == "result_processor":
                logging.debug("Checking result processor")
                # Check that the tool output is in the messages
                assert state["messages"][-1].content == state["tool_outputs"][0]
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
