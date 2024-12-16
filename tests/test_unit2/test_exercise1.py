import json
import logging
from typing import Any

import pytest

# Configure logging
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_exercise_2_1(student_submission: Any) -> None:
    """Check that the student has implemented the simple tool user correctly."""
    try:
        graph = student_submission.graph
    except AttributeError:
        # Try to be slightly more robust in case the student forgets to name it 'graph'
        graph = student_submission

    # Initialize with empty state containing required fields
    inputs = {
        "messages": [],
        "tool_calls": [],
        "tool_outputs": [],
    }

    # Track what we've seen through the graph execution
    seen_messages = []
    seen_tool_calls = []
    seen_tool_outputs = []

    # Stream all values to check state transitions
    async for event in graph.astream(inputs, stream_mode="values"):
        logger.debug(f"Processing event: {event}")

        # Track messages
        if "messages" in event:
            seen_messages.extend(
                msg for msg in event["messages"] if msg not in seen_messages
            )

            # Check initial message
            if len(seen_messages) == 1:
                logger.debug("Checking initial message")
                assert seen_messages[0].content == "What is the capital of France?"

        # Track tool calls
        if event.get("tool_calls"):
            call = event["tool_calls"][0]
            if call not in seen_tool_calls:
                seen_tool_calls.append(call)
                logger.debug("Checking tool call")
                assert call == {
                    "tool_name": "TavilySearchResults",
                    "args": {"query": "capital of France"},
                }

        # Track tool outputs
        if event.get("tool_outputs"):
            output = event["tool_outputs"][0]
            if output not in seen_tool_outputs:
                seen_tool_outputs.append(output)
                logger.debug("Checking tool output")
                try:
                    json.loads(output)
                except json.JSONDecodeError as err:
                    raise AssertionError("Tool output is not valid JSON") from err

    # Verify we saw all required parts
    assert len(seen_messages) >= 2, "Should see at least initial and final messages"
    assert len(seen_tool_calls) >= 1, "Should see at least one tool call"
    assert len(seen_tool_outputs) >= 1, "Should see at least one tool output"

    # Check final message content
    assert any(
        "Thanks for the information!" in msg.content for msg in seen_messages
    ), "Should end with thank you message"

    # Verify we can get final output
    final_output = await graph.ainvoke(inputs)
    assert final_output is not None
