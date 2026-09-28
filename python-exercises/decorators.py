import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time} seconds")
        return result
    return wrapper

def validate_grades(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for grade in args[0]:
            if grade < 0 or grade > 100:
                raise ValueError("Grades must be greater than 0 and less than 100")
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":
    @timer
    def add(a, b):
        return a + b
    print(add(2, 3))

    @validate_grades
    def process_grades(grades: list[int]) -> float:
        return sum(grades) / len(grades)
    valid_grades = process_grades([0, 50, 100])
    print(valid_grades)
    invalid_grades = process_grades([-5, 50, 110])

