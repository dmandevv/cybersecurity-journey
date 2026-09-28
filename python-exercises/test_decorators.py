import pytest
import time
from decorators import timer, validate_grades

def test_timer_return_value():
    @timer
    def add(a, b):
        return a + b
    assert add(2, 3) == 5

def test_valid_grades():
    @validate_grades
    def process_grades(grades: list[int]) -> float:
        return sum(grades) / len(grades)
    assert process_grades([0, 100]) == 50.0

def test_invalid_grades():
    @validate_grades
    def process_grades(grades: list[int]) -> float:
        return sum(grades) / len(grades)
    with pytest.raises(ValueError):
        process_grades([-5, 100])
    with pytest.raises(ValueError):
        process_grades([0, 110])
    