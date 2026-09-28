import pytest
import os
from grade_book import save_grade_book, load_grade_book
from student_report import Student

def test_save_grade_book(tmp_path):
    filepath = str(tmp_path / "grades.json")
    students = [Student("Student1", [100, 90, 80]), Student("Student2", [10, 30, 60])]
    save_grade_book(students, filepath)
    assert os.path.exists(filepath)

def test_load_grade_book(tmp_path):
    filepath = str(tmp_path / "grades.json")
    students = [Student("Student1", [100, 90, 80]), Student("Student2", [10, 30, 60])]
    save_grade_book(students, filepath)
    loaded = load_grade_book(filepath)
    assert loaded == students

def test_load_missing_grade_book(tmp_path):
    with pytest.raises(FileNotFoundError):
        filepath = str(tmp_path / "grades.json")
        load_grade_book(filepath)