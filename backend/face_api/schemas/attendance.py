from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time
from .user import StudentResponse, ProfessorResponse
from .class_schema import ClassResponse

class AttendanceBase(BaseModel):
    clase_id: int
    profesor_id: int
    fecha: date

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceDetailResponse(BaseModel):
    alumno: StudentResponse
    presente: bool

    class Config:
        orm_mode = True

class AttendanceResponse(AttendanceBase):
    id: int
    hora: time
    detalles: List[AttendanceDetailResponse] = []

    class Config:
        orm_mode = True

class MarkAttendanceRequest(BaseModel):
    clase_id: int
    image_base64: str # Or handle file upload separately
