from fastapi import FastAPI, HTTPException, Depends
from .models import StudentDB, Student, StudentUpdate
from .database import Base, engine, SessionLocal
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

app = FastAPI()

# dummy_student_data = {
#     100000: Student(name="Bob", grades=[]),
#     100001: Student(name="Alice", grades=[100, 100, 100, 100]),
#     100002: Student(name="Joe", grades=[55, 0]),
#     100003: Student(name="Bob", grades=[]),
# }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students", status_code=200)
def get_students(db: Session = Depends(get_db)):
    statement = select(StudentDB).order_by(StudentDB.name)
    results = db.execute(statement).scalars().all()
    return [{"id": student.id, "name":student.name, "grades":student.grades} for student in results]

@app.get("/students/{id}/average", status_code=200)
def get_student_grade_average(id: int, db: Session = Depends(get_db)):
    statement = select(StudentDB).where(StudentDB.id == id)
    student_db = db.execute(statement).scalar()
    if student_db is None:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    grades = [int(g.strip()) for g in student_db.grades.split(",")]
    student = Student(name=student_db.name, grades=grades)
    return {"name":student.name, "average":student.grade_average()}

@app.get("/students/{id}", status_code=200)
def get_student(id: int, db: Session = Depends(get_db)):
    statement = select(StudentDB).where(StudentDB.id == id)
    student_db = db.execute(statement).scalar()
    if student_db is None:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    grades = [int(g.strip()) for g in student_db.grades.split(",")]
    return {"id": student_db.id, "name":student_db.name, "grades":grades}

@app.post("/students", status_code=201)
def create_student(student: Student, db: Session = Depends(get_db)):
    grades_string = ",".join(map(str, student.grades))
    student_db = StudentDB(name=student.name, grades=grades_string)    
    db.add(student_db)
    db.commit()
    db.refresh(student_db)
    return {"id":student_db.id, "name":student_db.name, "grades":student_db.grades}

@app.put("/students/{id}", status_code=200)
def update_student(id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    update_data = student_update.model_dump(exclude_none=True)
    if "grades" in update_data:
        update_data["grades"] = ",".join(map(str, update_data["grades"]))
    statement = select(StudentDB).where(StudentDB.id == id)
    student_db = db.execute(statement).scalar()
    if student_db is None:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    for field, value in update_data.items():
        setattr(student_db, field, value)
    db.commit()
    db.refresh(student_db)
    return {"id":student_db.id, "name":student_db.name, "grades":student_db.grades}

@app.delete("/students/{id}", status_code=204)
def delete_student(id: int, db: Session = Depends(get_db)):
    statement = delete(StudentDB).where(StudentDB.id == id)
    result = db.execute(statement)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    db.commit()

