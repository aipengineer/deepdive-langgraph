from langchain_core.messages import ChatMessage, HumanMessage

# Import the graph from the exercise file
from src.exercises.unit2.exercise3 import graph


def test_exercise3():
    # Test that the chat bot is able to respond to the user coherently
    # We can invoke the graph with a human message
    result = graph.invoke(
        {
            "messages": [HumanMessage(content="Hello!")],
            "pending_tools": [],
            "results": {},
            "errors": {},
            "tool_code": None,
        }
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


# Test the correctness of the execution
def test_exercise3_correctness():
    # Test the executor with valid tool calls
    tool_inputs = [
        {"destination": "New York"},
        {"location": "London"},
        {"pickup_location": "Paris"},
    ]
    results = executor.execute(tool_inputs)
    assert results == {
        "search_flights": "Flights to New York",
        "search_hotels": "Hotels in London",
        "search_car_rentals": "Car rentals in Paris",
    }


# Test the error handling capability
def test_exercise3_error_handling():
    # Test the executor with one tool raising an exception
    tool_inputs = [
        {"destination": "New York"},
        {"location": "London"},
        {"pickup_location": 123},  # This will raise a TypeError
    ]
    results = executor.execute(tool_inputs)
    assert "search_flights" in results
    assert "search_hotels" in results
    assert "search_car_rentals" in results
    assert isinstance(results["search_car_rentals"], str)
    assert results["search_car_rentals"].startswith("Error:")
