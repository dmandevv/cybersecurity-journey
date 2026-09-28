import pytest
from pipeline import read_grades, filter_passing, compute_average
from grade_book import save_grade_book, load_grade_book
from student_report import Student

students = [Student("S1", [0, 10, 20]), Student("S2", [20, 60, 100])]

def test_read_grades(tmp_path):
    filepath = str(tmp_path / "grades.json")
    save_grade_book(students, filepath)

    gen = read_grades(filepath)
    assert next(gen) == students[0]
    assert next(gen) == students[1]

def test_filter_passing(tmp_path):
    filepath = str(tmp_path / "grades.json")
    save_grade_book(students, filepath)

    gen = filter_passing(read_grades(filepath), 50.0)
    assert next(gen) == students[1] # first student is failing

def test_compute_average(tmp_path):
    filepath = str(tmp_path / "grades.json")
    save_grade_book(students, filepath)

    gen = compute_average(read_grades(filepath))
    assert next(gen) == ("S1", 10.0)
    assert next(gen) == ("S2", 60.0)

def test_passing_average(tmp_path):
    filepath = str(tmp_path / "grades.json")
    save_grade_book(students, filepath)

    gen = compute_average(filter_passing(read_grades(filepath)))
    assert next(gen) == ("S2", 60.0)
    with pytest.raises(StopIteration):
        next(gen)

    
