# Python Fundamentals

Step 1 of my [SOC Python Journey](https://github.com/dmandevv/soc-python-journey).

Python fundamentals — type hints, decorators, generators, file I/O — plus a FastAPI CRUD app and a Vigenère cipher cracking exercise.

---

## Exercises

| File | Concepts covered |
|---|---|
| `grade_book.py` | Type hints, dataclasses, list comprehensions, JSON I/O |
| `student_report.py` | File I/O, context managers, data formatting |
| `pipeline.py` | Generators, chaining data transformations |
| `decorators.py` | Writing and applying decorators, `functools.wraps` |

Each has a matching `test_*.py`, run with pytest.

## FastAPI CRUD App

[`fastapi_app/`](fastapi_app/) — a fully functional REST API:

- `POST /items`, `GET /items`, `GET /items/{id}`, `PUT /items/{id}`, `DELETE /items/{id}`
- SQLAlchemy ORM with SQLite, Pydantic request/response models
- Dependency injection for DB sessions
- pytest integration tests with a real in-memory test database (not mocked)
- Async route handlers

## VigCipher

[`VigCipher/`](VigCipher/) — cracking a Vigenère-encrypted message via frequency analysis.

---

## Topics covered

- [x] Type hints, dataclasses, properties
- [x] List comprehensions, generators
- [x] File I/O, JSON, context managers
- [x] Decorators
- [x] pytest — unit and integration testing
- [x] FastAPI, Pydantic, SQLAlchemy
- [x] REST API design, dependency injection, async basics
- [x] Classical cipher cracking via frequency analysis
