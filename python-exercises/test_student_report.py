from student_report import Student, average, passing_students, top_student
import pytest

def test_create_student_normal():
    s = Student("Student", [50, 60, 90])
    assert s.grades == [50, 60, 90]

def test_create_student_invalid_grades():
    with pytest.raises(ValueError):
        Student("Student", [50, 160, 90])
    
def test_average_normal():
    assert average([90, 80, 70]) == 80.0

def test_average_empty():
    assert average([]) == 0

def test_average_single():
    assert average([50]) == 50.0

def test_passing_students_normal():
    s1 = Student("Student1", [10, 20])
    s2 = Student("Student2", [80, 90])
    assert passing_students([s1, s2], 50) == [s2]

def test_passing_students_empty():
    assert passing_students([], 50) == []

def test_top_student_normal():
    top = Student("Student1", [100, 100])
    middle = Student("Student2", [80, 90])
    bottom = Student("Student3", [30, 20, 60])
    assert top_student([top, middle, bottom]) == top

def test_top_student_empty():
    with pytest.raises(ValueError):
        top_student([])