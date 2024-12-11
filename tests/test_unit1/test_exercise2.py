from langchain_core.messages import HumanMessage, ChatMessage

# Import the graph from the exercise file
from src.exercises.unit1.exercise2 import graph

def test_exercise2():
    # Test that the chat bot is able to respond to the user coherently over multiple turns.
    # We can invoke the graph with a human message
    result = graph.invoke({"messages": [HumanMessage(content="Hello!")], "summary": "N/A", "window_size": 5})
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

    # Continue the conversation coherently
    result = graph.invoke({**result, "messages": [HumanMessage(content="My name is Harrison.")]})
    assert "Harrison" in result["messages"][-1].content

    result = graph.invoke({**result, "messages": [HumanMessage(content="What's the weather like in SF?")]})
    assert "weather" in result["messages"][-1].content