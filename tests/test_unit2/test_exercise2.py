"""
Tests for Exercise 2.2 - Multi-Tool Agent Solution
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
    """Test the calculator tool implementation."""
    calculator = student_submission.calculator

    # Test basic arithmetic
    assert calculator("2 + 2") == "4.0"
    assert calculator("10 * 5") == "50.0"
    assert calculator("100 / 25") == "4.0"
    assert calculator("2 ** 3") == "8.0"

    # Test with mathematical constants
    assert float(calculator("pi")) > 3.14
    assert float(calculator("e")) > 2.71

    # Test error handling
    result = calculator("invalid")
    assert "Error" in result
    assert "evaluating expression" in result


@pytest.mark.asyncio
async def test_weather(student_submission: Any) -> None:
    """Test the weather tool implementation."""
    check_weather = student_submission.check_weather

    # Test basic weather query
    result = check_weather("London")
    assert isinstance(result, str)
    assert "sunny" in result.lower()
    assert "London" in result

    # Test with cleaned location
    result = check_weather(" New York ")  # with spaces
    assert "New York" in result


@pytest.mark.asyncio
async def test_tool_selector(student_submission: Any) -> None:
    """Test the tool selection logic."""
    tool_selector = student_submission.tool_selector

    # Test initialization
    initial_state = tool_selector({"messages": []})
    assert len(initial_state["available_tools"]) == 3
    assert all(count == 0 for count in initial_state["tool_usage"].values())

    # Test tool selection
    weather_state = {
        "messages": [HumanMessage(content="What's the weather in Paris?")],
        "available_tools": initial_state["available_tools"],
        "tool_usage": initial_state["tool_usage"].copy(),
        "rate_limits": initial_state["rate_limits"],
    }
    result = tool_selector(weather_state)
    assert result["tool_name"] == "check_weather"

    # Test calculator selection
    math_state = {
        "messages": [HumanMessage(content="Calculate 15 + 25")],
        "available_tools": initial_state["available_tools"],
        "tool_usage": initial_state["tool_usage"].copy(),
        "rate_limits": initial_state["rate_limits"],
    }
    result = tool_selector(math_state)
    assert result["tool_name"] == "calculator"

    # Test search selection
    search_state = {
        "messages": [HumanMessage(content="Who invented the telephone?")],
        "available_tools": initial_state["available_tools"],
        "tool_usage": initial_state["tool_usage"].copy(),
        "rate_limits": initial_state["rate_limits"],
    }
    result = tool_selector(search_state)
    assert result["tool_name"] == "TavilySearchResults"


@pytest.mark.asyncio
async def test_rate_limits(student_submission: Any) -> None:
    """Test rate limiting functionality."""
    tool_selector = student_submission.tool_selector

    # Initialize state
    initial_state = tool_selector({"messages": []})
    weather_query = HumanMessage(content="What's the weather in London?")

    state = {
        "messages": [weather_query],
        "available_tools": initial_state["available_tools"],
        "tool_usage": initial_state["tool_usage"],
        "rate_limits": initial_state["rate_limits"],
    }

    # Use weather tool until limit
    limit = state["rate_limits"]["check_weather"]
    for _ in range(limit):
        result = tool_selector(state)
        assert result["tool_name"] == "check_weather"
        state["tool_usage"]["check_weather"] += 1

    # Verify rate limit enforcement
    result = tool_selector(state)
    assert "messages" in result
    assert "Rate limit exceeded" in result["messages"][-1].content


@pytest.mark.asyncio
async def test_tool_executor(student_submission: Any) -> None:
    """Test tool execution functionality."""
    tool_executor = student_submission.tool_executor

    # Test calculator execution
    calc_state = {
        "tool_name": "calculator",
        "messages": [HumanMessage(content="Calculate 2 + 2")],
        "available_tools": [student_submission.calculator],
    }
    result = tool_executor(calc_state)
    assert "tool_outputs" in result
    assert "4.0" in result["tool_outputs"][0]

    # Test weather execution
    weather_state = {
        "tool_name": "check_weather",
        "messages": [HumanMessage(content="What's the weather in Tokyo?")],
        "available_tools": [student_submission.check_weather],
    }
    result = tool_executor(weather_state)
    assert "tool_outputs" in result
    assert "Tokyo" in result["tool_outputs"][0]


@pytest.mark.asyncio
async def test_get_next_step(student_submission: Any) -> None:
    """Test the conversation flow control logic."""
    get_next_step = student_submission.get_next_step

    # Test empty state
    empty_state = {"messages": []}
    assert get_next_step(empty_state) == "end"

    # Test continuing conversation
    continue_state = {"messages": [HumanMessage(content="What's 2+2?")]}
    assert get_next_step(continue_state) == "tool_selector"

    # Test ending conversation
    end_state = {"messages": [HumanMessage(content="Thanks for your help!")]}
    assert get_next_step(end_state) == "end"


@pytest.mark.asyncio
async def test_full_conversation(student_submission: Any) -> None:
    """Test a complete conversation flow."""
    graph = student_submission.graph

    # Test initial greeting
    initial_result = await graph.ainvoke({"messages": []})
    assert "How can I help you" in initial_result["messages"][-1].content

    # Test calculator usage
    calc_result = await graph.ainvoke(
        {"messages": [HumanMessage(content="Calculate 25 * 4")]}
    )
    assert "100" in str(calc_result["messages"][-1].content)

    # Test weather query
    weather_result = await graph.ainvoke(
        {"messages": [HumanMessage(content="What's the weather in Paris?")]}
    )
    assert "Paris" in str(weather_result["messages"][-1].content)

    # Test conversation ending
    end_result = await graph.ainvoke(
        {"messages": [HumanMessage(content="Thanks for your help!")]}
    )
    assert "welcome" in end_result["messages"][-1].content.lower()


@pytest.fixture
def base_state():
    """Provide a base state for testing."""
    return {
        "messages": [],
        "available_tools": [],
        "tool_usage": {},
        "rate_limits": {},
    }
