import json
import os
from student_report import Student

def save_grade_book(students: list[Student], filepath: str) -> None:
    with open(filepath, "w") as file:
        data = [{"name": s.name, "grades": s.grades} for s in students]
        json.dump(data, file)

def load_grade_book(filepath: str) -> list[Student]:
    with open(filepath, "r") as file:
        data = json.load(file)
        return [Student(d["name"], d["grades"]) for d in data]