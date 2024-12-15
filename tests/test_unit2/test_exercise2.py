from langchain_core.messages import HumanMessage

# Import the graph from the exercise file
from src.exercises.unit2.exercise2 import graph


def test_exercise2():
    # Initialize the conversation with a greeting
    result = graph.invoke(
        {
            "messages": [HumanMessage(content="Hello!")],
            "available_tools": [
                graph.nodes["search"],
                graph.nodes["calculator"],
                graph.nodes["weather"],
            ],
            "tool_usage": {},
            "rate_limits": {"search": 2, "calculator": 3, "weather": 1},
            "tool_code": None,
        }
    )
    assert isinstance(result, dict)
    assert "messages" in result
    assert isinstance(result["messages"], list)
    assert len(result["messages"]) > 0
    assert isinstance(result["messages"][-1], AIMessage)
    assert result["messages"][-1].content

    # Ask a question that requires the search tool
    result = graph.invoke(
        {
            **result,
            "messages": [HumanMessage(content="What is the capital of France?")],
        }
    )
    assert isinstance(result["messages"][-1], AIMessage)
    assert result["messages"][-1].content.startswith("tool_code:")

    # Ask a math question that requires the calculator tool
    result = graph.invoke(
        {
            **result,
            "messages": [HumanMessage(content="What is 2 plus 2?")],
        }
    )
    assert isinstance(result["messages"][-1], AIMessage)
    assert result["messages"][-1].content.startswith("tool_code:")

    # Ask a weather question that requires the weather tool
    result = graph.invoke(
        {
            **result,
            "messages": [HumanMessage(content="What is the weather in London?")],
        }
    )
    assert isinstance(result["messages"][-1], AIMessage)
    assert result["messages"][-1].content.startswith("tool_code:")

    # Test rate limiting for the search tool
    result = graph.invoke(
        {
            **result,
            "messages": [HumanMessage(content="What is the capital of France?")],
        }
    )
    result = graph.invoke(
        {
            **result,
            "messages": [HumanMessage(content="What is the capital of France?")],
        }
    )
    assert "I've reached the usage limit for search" in result["messages"][-1].content
