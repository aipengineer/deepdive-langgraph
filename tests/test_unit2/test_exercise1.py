from langchain_core.messages import ChatMessage, HumanMessage

# Import the graph from the exercise file
from src.exercises.unit2.exercise1 import graph


def test_exercise1():
    # Test that the chat bot is able to respond to the user coherently
    # We can invoke the graph with a human message
    result = graph.invoke(
        {"messages": [HumanMessage(content="Hello!")], "tool_code": None}
    )
    # The result should be a dict
    assert isinstance(result, dict)
    # The result should have a key "messages"
    assert "messages" in result
    # The messages should be a list
    assert isinstance(result["messages"], list)
    # The list should not be empty
    assert len(result["messages"]) > 0
    # The last message should be a ChatMessage
    assert isinstance(result["messages"][-1], ChatMessage)
    # The message content should not be empty
    assert result["messages"][-1].content

    # Test that the tool is called when needed
    result = graph.invoke(
        {
            "messages": [HumanMessage(content="What flights are available to Paris?")],
            "tool_code": None,
        }
    )
    # Check if a ToolMessage is present in the response, indicating the tool was called
    assert any(isinstance(message, ToolMessage) for message in result["messages"])

    # Test that the tool output is processed correctly
    # (This might need adjustment based on the actual tool output)
    # Check if an AIMessage containing "Paris" is present, indicating successful processing
    assert any(
        "Paris" in message.content
        for message in result["messages"]
        if isinstance(message, AIMessage)
    )
