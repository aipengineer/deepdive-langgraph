import os
import sys
import pytest
from pathlib import Path

# Add the solutions directory to the Python path
solutions_path = Path(__file__).parent.parent / "solutions"
sys.path.append(str(solutions_path))


def get_solution_module(request):
    """
    Dynamically import the solution module based on the test path.
    Example: if test is in test_unit1/test_exercise1.py,
    import solution from unit1/exercise1.py
    """
    test_path = request.module.__file__
    test_path = Path(test_path)

    # Extract unit and exercise numbers from test path
    # e.g., from 'test_unit1/test_exercise1.py' get 'unit1' and 'exercise1'
    unit_name = test_path.parent.name.replace('test_', '')
    exercise_name = test_path.stem.replace('test_', '')

    # Import the corresponding solution module
    solution_module = __import__(
        f"{unit_name}.{exercise_name}",
        fromlist=['*']
    )

    return solution_module


@pytest.fixture
def student_submission(request):
    """
    Fixture that provides the student's solution module for each test.
    """
    try:
        return get_solution_module(request)
    except ImportError as e:
        pytest.skip(f"Solution module not found: {e}")