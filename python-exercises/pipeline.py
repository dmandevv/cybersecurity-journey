from grade_book import load_grade_book
from student_report import average

def read_grades(filepath: str):
    for student in load_grade_book(filepath):
        yield student

def filter_passing(students, threshold: float = 50.0):
    for student in students:
        if average(student.grades) >= threshold:
            yield student

def compute_average(students):
    for student in students:
        yield (student.name, average(student.grades))

if __name__ == "__main__":
    from grade_book import save_grade_book
    from student_report import Student

    students = [
        Student("Alice", [90, 85, 92]),
        Student("Bob", [30, 40, 35]),
        Student("Charlie", [70, 65, 80]),
    ]

    save_grade_book(students, "test_grades.json")

    for (name, avg) in compute_average(filter_passing(read_grades("test_grades.json"))):
        print(f"{name}: {avg:.1f}")