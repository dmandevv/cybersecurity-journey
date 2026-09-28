from dataclasses import dataclass

@dataclass
class Student:
    name: str
    _grades: list[int]

    def __post_init__(self):
        self.grades = self._grades
    
    @property
    def grades(self) -> list[int]:
        return self._grades

    @grades.setter
    def grades(self, grades: list[int]):
        if any(g < 0 or g > 100 for g in grades):
            raise ValueError("Grades must be between 0 and 100")
        self._grades = grades

def average(grades: list[int]) -> float:
    if not grades:
        return 0.0
    return sum(grades) / len(grades)

def passing_students(students: list[Student], threshold: float = 50.0) -> list[Student]:
    return [student for student in students if average(student.grades) >= threshold]

def top_student(students: list[Student]) -> Student:
    if not students:
        raise ValueError("Cannot determine top student from an empty list")
    return max(students, key=lambda s: average(s.grades))
