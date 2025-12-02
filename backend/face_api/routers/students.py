from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import numpy as np
import cv2
import json
from ..database import get_db
from ..models import sql_models as models
from ..schemas import user as schemas
from ..services.face_recognition import FaceRecognizer

router = APIRouter(
    prefix="/alumnos",
    tags=["alumnos"]
)

# Initialize FaceRecognizer (singleton or dependency)
# Ideally, this should be a dependency injection or a global instance initialized at startup
face_recognizer = FaceRecognizer(model_dir="models")

@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.codigo == student.codigo).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student code already registered")
    new_student = models.Student(nombre=student.nombre, codigo=student.codigo)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/", response_model=List[schemas.StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@router.post("/{student_id}/register-face")
async def register_face(student_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Read image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    # Detect and align
    faces = face_recognizer.detect_faces(img)
    if not faces:
        raise HTTPException(status_code=400, detail="No face detected")
    
    # Assume the largest face is the target or take the first one
    # Ideally, check for multiple faces and warn
    target_face = faces[0]
    aligned_face = face_recognizer.align_face(img, target_face['kps'])
    
    # Get embedding
    embedding = face_recognizer.get_embedding(aligned_face)
    if embedding is None:
        raise HTTPException(status_code=500, detail="Failed to extract embedding")

    # Save embedding to DB (as JSON string)
    student.embedding = json.dumps(embedding.tolist())
    db.commit()
    
    return {"message": "Face registered successfully"}
