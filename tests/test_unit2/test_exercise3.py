import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_2_3(student_submission):
    """Check that the student has implemented the parallel tool executor correctly."""
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
            if name == "parallel_executor":
                if not state.get("pending_tools"):
                    logging.debug("First time, no pending tools")
                    assert state["pending_tools"] == [
                        {
                            "tool_name": "TavilySearchResults",
                            "args": {"query": "capital of France"},
                        },
                        {"tool_name": "LLMMathChain", "args": "2 + 2"},
                        {
                            "tool_name": "WeatherSearchTool",
                            "args": {"query": "weather in London"},
                        },
                    ]
                    assert state["results"] == {}
                    assert state["errors"] == {}
                else:
                    logging.debug("Second time, should have results and/or errors")
                    assert len(state["results"]) + len(state["errors"]) == 3
            elif name == "result_aggregator":
                logging.debug("Checking result aggregator")
                # Check that the results are in the messages
                for tool_name, result in state["results"].items():
                    assert any(
                        tool_name in message.content and str(result) in message.content
                        for message in state["messages"]
                    )
            elif name == "error_handler":
                logging.debug("Checking error handler")
                # Check that the errors are in the messages
                for tool_name, error in state["errors"].items():
                    assert any(
                        tool_name in message.content and error in message.content
                        for message in state["messages"]
                    )
            else:
                raise ValueError(f"Unknown step: {name}")
        # For debugging, you can view the full execution in the LangSmith app at the
        # provided URL
        # print(f"Step: {step}")
    # Check that the final output is in the correct format
    # (for this exercise, the format is unimportant)
    final_output = graph.invoke(inputs)
    assert final_output
