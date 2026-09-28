from pydantic import BaseModel, field_validator
from sqlalchemy import Column, Integer, String
from .database import Base

class Student(BaseModel):
    name: str
    grades: list[int]

    @field_validator("name")
    @classmethod
    def validate_name(cls, name):
        if not 1 <= len(name) <= 50:
            raise ValueError("Name must be between 1 and 50 characters")
        return name

    @field_validator("grades")
    @classmethod
    def validate_grades(cls, grades):
        if any(g < 0 or g > 100 for g in grades):
            raise ValueError("Grades must be between 0 and 100")
        return grades
    

    def grade_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

class StudentUpdate(BaseModel):
    name: str | None = None
    grades: list[int] | None = None

class StudentDB(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    grades = Column(String, nullable=False)

