"""
Test suite for Exercise 2.3 - Parallel Tool Executor
"""

import logging
from typing import Any

import pytest
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_parallel_execution_flow(student_submission: Any) -> None:
    """Test the complete parallel execution flow."""
    try:
        graph = student_submission.graph
    except AttributeError:
        pytest.fail("Could not find graph in student submission")

    # Run the graph
    result = await graph.ainvoke({})

    # Verify structure
    assert "messages" in result
    assert "results" in result
    assert "errors" in result

    # Check messages
    messages = [m.content for m in result["messages"]]
    assert any("capital of France" in m for m in messages)
    assert any("largest city in Japan" in m for m in messages)


@pytest.mark.asyncio
async def test_error_handling(student_submission: Any) -> None:
    """Test error handling in parallel execution."""
    try:
        graph = student_submission.graph
    except AttributeError:
        pytest.fail("Could not find graph in student submission")

    # Create a state with an invalid tool call
    input_state = {
        "messages": [],
        "pending_tools": [{
            "id": "invalid_search",
            "tool_name": "TavilySearchResults",
            "args": {},  # Invalid args to trigger error
        }],
        "results": {},
        "errors": {},
    }

    # Run the graph
    result = await graph.ainvoke(input_state)

    # Verify error handling
    assert "errors" in result
    assert len(result["errors"]) > 0
    assert any("Error" in m.content for m in result["messages"])


@pytest.mark.asyncio
async def test_result_aggregation(student_submission: Any) -> None:
    """Test that results are properly aggregated."""
    try:
        graph = student_submission.graph
    except AttributeError:
        pytest.fail("Could not find graph in student submission")

    # Run with default input
    result = await graph.ainvoke(student_submission.default_input)

    # Verify results
    messages = [m.content for m in result["messages"]]

    # Check for results from both searches
    search_results = [m for m in messages if "Result from search_" in m]
    assert len(search_results) > 0, "No search results found in messages"

    # Verify message format
    for msg in search_results:
        assert "Result from search_" in msg
        assert "{" in msg and "}" in msg, "Result should contain JSON data"


@pytest.mark.asyncio
async def test_state_consistency(student_submission: Any) -> None:
    """Test that state is maintained consistently throughout execution."""
    try:
        graph = student_submission.graph
    except AttributeError:
        pytest.fail("Could not find graph in student submission")

    result = await graph.ainvoke({})

    # Check state structure
    assert isinstance(result, dict)
    assert all(key in result for key in ["messages", "pending_tools", "results", "errors"])

    # Verify state consistency
    assert len(result["results"]) + len(result["errors"]) == len(result["pending_tools"])
    assert all(isinstance(msg.content, str) for msg in result["messages"])