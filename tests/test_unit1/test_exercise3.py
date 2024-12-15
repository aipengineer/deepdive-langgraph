import logging

from langchain_core.messages import HumanMessage

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_1_3(student_submission):
    """Check that the student has implemented the conditional router correctly."""
    try:
        graph = student_submission.graph
    except AttributeError:
        # Try to be slightly more robust in case the student forgets to name it 'graph'
        graph = student_submission

    # Test case 1: Greeting
    inputs = {"messages": [HumanMessage(content="Hello")]}
    state = graph.invoke(inputs)
    assert state["messages"][-1].content == "Hello there!"

    # Test case 2: Help
    inputs = {"messages": [HumanMessage(content="I need help")]}
    state = graph.invoke(inputs)
    assert state["messages"][-1].content == "How can I help you?"

    # Test case 3: Unknown
    inputs = {"messages": [HumanMessage(content="Foo bar")]}
    state = graph.invoke(inputs)
    assert state["messages"][-1].content == "I don't understand."
