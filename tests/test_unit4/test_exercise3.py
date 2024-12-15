import logging

from langchain_core.messages import HumanMessage

# The logger is used to check that the nodes
# are doing the right work
logger = logging.getLogger(__name__)


def test_exercise_4_3(student_submission):
    """Check that the student has implemented the dynamic routing correctly."""
    try:
        graph = student_submission.graph
    except AttributeError:
        # Try to be slightly more robust in case the student forgets to name it 'graph'
        graph = student_submission

    # Test case 1: Choose path A, then confirm
    inputs = [HumanMessage(content="A"), HumanMessage(content="Yes")]
    state = graph.invoke(inputs)
    assert state["routing_history"] == ["A", "A"]
    assert state["suggestions"] == ["Path A is recommended.", "Think carefully."]

    # Test case 2: Choose path A, then change to B
    inputs = [HumanMessage(content="A"), HumanMessage(content="No")]
    state = graph.invoke(inputs)
    assert state["routing_history"] == ["A", "B"]
    assert state["suggestions"] == ["Path A is recommended.", "Think carefully."]

    # Test case 3: Choose path B directly
    inputs = [HumanMessage(content="B")]
    state = graph.invoke(inputs)
    assert state["routing_history"] == ["B"]
    assert state["suggestions"] == ["Path A is recommended."]
