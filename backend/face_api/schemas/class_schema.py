from pydantic import BaseModel
from typing import Optional, List
from .user import ProfessorResponse, StudentResponse

class ClassBase(BaseModel):
    nombre: str
    profesor_id: int

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: int
    profesor: Optional[ProfessorResponse] = None
    # alumnos: List[StudentResponse] = [] # Optional to include students

    class Config:
        orm_mode = True

class AssignStudentRequest(BaseModel):
    alumno_id: int
