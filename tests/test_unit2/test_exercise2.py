"""
Tests for Exercise 2.2 - Multi-Tool Agent

This test suite verifies:
1. Individual tool functionality
2. Tool selection and execution
3. Rate limiting
4. Full conversation flow
"""

import logging
from typing import Any

import pytest
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_calculator(student_submission: Any) -> None:
    """Test calculator functionality and integration."""
    calculator = student_submission.calculator
    tool_executor = student_submission.tool_executor
    State = student_submission.State

    calc_state: State = {
        "messages": [HumanMessage(content="Calculate 2 + 2")],
        "available_tools": [calculator],
        "tool_usage": {},
        "rate_limits": {},
        "tool_name": "calculator",
        "tool_outputs": []
    }

    result = tool_executor(calc_state)
    assert "4.0" in str(result["tool_outputs"][0])

    # Test with mathematical constants
    calc_state["messages"] = [HumanMessage(content="Calculate pi")]
    result = tool_executor(calc_state)
    assert float(str(result["tool_outputs"][0])) > 3.14

    # Test error handling
    calc_state["messages"] = [HumanMessage(content="Calculate invalid")]
    result = tool_executor(calc_state)
    assert "Error" in str(result["tool_outputs"][0])


@pytest.mark.asyncio
async def test_weather(student_submission: Any) -> None:
    """Test weather tool functionality and integration."""
    check_weather = student_submission.check_weather
    tool_executor = student_submission.tool_executor
    State = student_submission.State

    weather_state: State = {
        "messages": [HumanMessage(content="What's the weather in London?")],
        "available_tools": [check_weather],
        "tool_usage": {},
        "rate_limits": {},
        "tool_name": "check_weather",
        "tool_outputs": []
    }

    result = tool_executor(weather_state)
    assert "sunny" in str(result["tool_outputs"][0]).lower()
    assert "London" in str(result["tool_outputs"][0])


@pytest.mark.asyncio
async def test_full_conversation(student_submission: Any) -> None:
    """Test complete conversation flow."""
    graph = student_submission.graph

    # Test calculator usage
    result = await graph.ainvoke({
        "messages": [HumanMessage(content="Calculate 25 * 4")],
        "available_tools": [student_submission.calculator],
        "tool_usage": {},
        "rate_limits": {}
    })
    assert any("100" in str(msg.content) for msg in result["messages"])

    # Test weather query
    result = await graph.ainvoke({
        "messages": [HumanMessage(content="What's the weather in Paris?")],
        "available_tools": [student_submission.check_weather],
        "tool_usage": {},
        "rate_limits": {}
    })
    assert any("Paris" in str(msg.content) for msg in result["messages"])


@pytest.mark.asyncio
async def test_rate_limits(student_submission: Any) -> None:
    """Test rate limiting functionality."""
    tool_selector = student_submission.tool_selector
    State = student_submission.State

    initial_state: State = {
        "messages": [HumanMessage(content="What's the weather in London?")],
        "available_tools": [student_submission.check_weather],
        "tool_usage": {"check_weather": 0},
        "rate_limits": {"check_weather": 1},
        "tool_outputs": []
    }

    # First call should work
    result = tool_selector(initial_state)
    assert result["tool_name"] == "check_weather"

    # Second call should hit rate limit
    result["tool_usage"]["check_weather"] = 1
    result = tool_selector(result)
    assert "Rate limit exceeded" in result["messages"][-1].content