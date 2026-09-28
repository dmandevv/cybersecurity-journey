from fastapi.testclient import TestClient
from .main import app

client = TestClient(app=app)

def test_get_students(created_student):
    res = client.get("/students")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert isinstance(data, list)
    assert {"id": created_student["id"], "name": "Bob", "grades": '20,50,80'} in data

def test_get_students_empty():
    res = client.get("/students")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_student_by_id(created_student):
    id = created_student["id"]
    res = client.get(f"/students/{id}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert isinstance(data, dict)
    assert {"id": id, "name": "Bob", "grades": [20,50,80]} == data

def test_get_student_by_id_missing():
    res = client.get("/students/404")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"

def test_get_student_average(created_student):
    id = created_student["id"]
    res = client.get(f"/students/{id}/average")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert {"name": "Bob", "average": 50.0} == data

def test_get_student_average_missing():
    res = client.get("/students/404/average")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"

def test_create_student():
    res = client.post("/students", json={"name": "Bob", "grades": [20, 50, 80]})
    assert res.status_code == 201, f"Expected 201, got {res.status_code}"
    data = res.json()
    assert data["name"] == "Bob"
    assert data["grades"] == "20,50,80"
    assert "id" in data

def test_update_student(created_student):
    id = created_student["id"]
    res = client.put(f"/students/{id}", json={"name": "Alice", "grades": [30, 60]})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert data == {"id": id, "name": "Alice", "grades": "30,60"}

def test_update_student_missing():
    res = client.put("/students/404", json={"name": "Alice", "grades": [30, 60]})
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"

def test_delete_student(created_student):
    id = created_student["id"]
    res = client.delete(f"/students/{id}")
    assert res.status_code == 204, f"Expected 204, got {res.status_code}"

def test_delete_student_missing():
    res = client.delete("/students/404")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"