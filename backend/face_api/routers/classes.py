from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import sql_models as models
from ..schemas import class_schema as schemas

router = APIRouter(
    prefix="/clases",
    tags=["clases"]
)

@router.post("/", response_model=schemas.ClassResponse)
def create_class(cls: schemas.ClassCreate, db: Session = Depends(get_db)):
    new_class = models.Class(nombre=cls.nombre, profesor_id=cls.profesor_id)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.get("/", response_model=List[schemas.ClassResponse])
def read_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classes = db.query(models.Class).offset(skip).limit(limit).all()
    return classes

@router.post("/{class_id}/assign-student")
def assign_student(class_id: int, assignment: schemas.AssignStudentRequest, db: Session = Depends(get_db)):
    # Check if class exists
    cls = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if student exists
    student = db.query(models.Student).filter(models.Student.id == assignment.alumno_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    # Check if already assigned
    exists = db.query(models.ClassStudent).filter(
        models.ClassStudent.clase_id == class_id,
        models.ClassStudent.alumno_id == assignment.alumno_id
    ).first()
    
    if exists:
        raise HTTPException(status_code=400, detail="Student already assigned to this class")
        
    new_assignment = models.ClassStudent(clase_id=class_id, alumno_id=assignment.alumno_id)
    db.add(new_assignment)
    db.commit()
    
    return {"message": "Student assigned successfully"}
