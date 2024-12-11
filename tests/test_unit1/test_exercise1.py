from langchain_core.messages import HumanMessage

# Import the graph from the exercise file
from src.exercises.unit1.exercise1 import graph

def test_exercise1():
    # We can invoke the graph with a human message
    result = graph.invoke({"messages": [HumanMessage(content="Hello!")]})
    # The result should be a dict
    assert isinstance(result, dict)
    # The result should have a key "messages"
    assert "messages" in result
    # The messages should be a list
    assert isinstance(result["messages"], list)
    # The list should not be empty
    assert len(result["messages"]) > 0
    # Check if the response is coherent
    assert "Hello" in result["messages"][0].content or "Hi" in result["messages"][0].content