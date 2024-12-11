from langchain_core.messages import HumanMessage, ChatMessage

# Import the graph from the exercise file
from src.exercises.unit1.exercise3 import graph

def test_exercise3():
    # Test that the chat bot is able to respond to the user coherently
    # We can invoke the graph with a human message
    result = graph.invoke({"messages": [HumanMessage(content="Hello!")], "classification": "not weather", "confidence": 0.8})
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

    # Test that the graph state is updated with the correct classification
    assert result["classification"] == "not weather"
    assert result["confidence"] == 0.9

    # Test that the graph routes the message to the correct node based on the classification
    assert result["messages"][-1].content == "The weather is not nice today. Last message: Hello!"

    # Test that the graph is able to handle edge cases, such as when the classification is not valid
    result = graph.invoke({"messages": [HumanMessage(content="What's the weather like in SF?")], "classification": "invalid", "confidence": 0.8})
    assert result["messages"][-1].content == "I'm sorry, I don't understand."

    # We can invoke the graph with a human message
    result = graph.invoke({"messages": [HumanMessage(content="What's the weather like in SF?")]})
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

    # Test that the graph state is updated with the correct classification
    assert result["classification"] == "weather"
    assert result["confidence"] == 0.9

    # Test that the graph routes the message to the correct node based on the classification
    assert result["messages"][-1].content == "The weather is nice today. Last message: What's the weather like in SF?"