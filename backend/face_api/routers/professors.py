from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import sql_models as models
from ..schemas import user as schemas

router = APIRouter(
    prefix="/profesores",
    tags=["profesores"]
)

@router.post("/", response_model=schemas.ProfessorResponse)
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    db_prof = db.query(models.Professor).filter(models.Professor.correo == professor.correo).first()
    if db_prof:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_hashed_password = professor.password + "notreallyhashed" # TODO: Hash password
    new_prof = models.Professor(nombre=professor.nombre, correo=professor.correo, password=fake_hashed_password)
    db.add(new_prof)
    db.commit()
    db.refresh(new_prof)
    return new_prof

@router.get("/", response_model=List[schemas.ProfessorResponse])
def read_professors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    professors = db.query(models.Professor).offset(skip).limit(limit).all()
    return professors
