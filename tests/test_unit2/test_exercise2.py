import json
import logging

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_2_2(student_submission):
    """Check that the student has implemented the multi-tool agent correctly."""
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
            if name == "tool_selector":
                if not state.get("available_tools"):
                    logging.debug("First time, no tools available")
                    assert len(state["available_tools"]) == 3
                    assert state["tool_usage"] == {
                        "TavilySearchResults": 0,
                        "LLMMathChain": 0,
                        "WeatherSearchTool": 0,
                    }
                    assert state["rate_limits"] == {
                        "TavilySearchResults": 2,
                        "LLMMathChain": 3,
                        "WeatherSearchTool": 1,
                    }
                else:
                    logging.debug("Second time, should have selected a tool")
                    message = state["messages"][-1].content
                    if "weather" in message.lower():
                        assert state["tool_name"] == "WeatherSearchTool"
                    elif any(
                        keyword in message.lower()
                        for keyword in ["calculate", "compute", "solve"]
                    ):
                        assert state["tool_name"] == "LLMMathChain"
                    else:
                        assert state["tool_name"] == "TavilySearchResults"
            elif name == "llm":
                if not state.get("messages"):
                    logging.debug("First time, no messages")
                    assert (
                        state["messages"][0].content
                        == "What is the weather in London today?"
                    )
                elif (
                    state["messages"][-1].content
                    == "What is the weather in London today?"
                ):
                    logging.debug("Second time, should have a math question")
                    assert state["messages"][-1].content == "Calculate 2 + 2"
                elif state["messages"][-1].content == "Calculate 2 + 2":
                    logging.debug("Third time, should have a search question")
                    assert (
                        state["messages"][-1].content
                        == "What is the capital of France?"
                    )
                else:
                    logging.debug("Fourth time, should have a thank you message")
                    assert (
                        state["messages"][-1].content == "Thanks for the information!"
                    )
            elif name == "tool_executor":
                logging.debug("Checking tool executor")
                # Check that the tool output is valid JSON (if applicable)
                try:
                    json.loads(state["tool_outputs"][0])
                except json.JSONDecodeError:
                    # If the output is not JSON, it should be a string
                    assert isinstance(state["tool_outputs"][0], str)
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
