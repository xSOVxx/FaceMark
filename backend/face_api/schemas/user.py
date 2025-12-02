from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Admin Schemas
class AdminBase(BaseModel):
    nombre: str
    correo: EmailStr

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int
    creado_en: datetime

    class Config:
        orm_mode = True

# Professor Schemas
class ProfessorBase(BaseModel):
    nombre: str
    correo: EmailStr

class ProfessorCreate(ProfessorBase):
    password: str

class ProfessorResponse(ProfessorBase):
    id: int
    creado_en: datetime

    class Config:
        orm_mode = True

# Student Schemas
class StudentBase(BaseModel):
    nombre: str
    codigo: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    creado_en: datetime
    # embedding is usually internal, maybe not expose it or expose as boolean "has_embedding"

    class Config:
        orm_mode = True
