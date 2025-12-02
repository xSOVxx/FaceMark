from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import numpy as np
import cv2
import json
from datetime import date, datetime
from ..database import get_db
from ..models import sql_models as models
from ..schemas import attendance as schemas
from ..services.face_recognition import FaceRecognizer

router = APIRouter(
    prefix="/asistencia",
    tags=["asistencia"]
)

# Initialize FaceRecognizer (singleton or dependency)
face_recognizer = FaceRecognizer(model_dir="models")

@router.post("/marcar", response_model=schemas.AttendanceResponse)
async def mark_attendance(
    clase_id: int = Form(...),
    profesor_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verify class and professor
    cls = db.query(models.Class).filter(models.Class.id == clase_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if attendance already exists for today
    today = date.today()
    attendance = db.query(models.Attendance).filter(
        models.Attendance.clase_id == clase_id,
        models.Attendance.fecha == today
    ).first()
    
    if not attendance:
        # Create new attendance record
        attendance = models.Attendance(clase_id=clase_id, profesor_id=profesor_id, fecha=today)
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
    
    # Process image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")
        
    # Detect faces
    faces = face_recognizer.detect_faces(img)
    if not faces:
        return attendance # No faces found, return empty attendance
        
    # Get registered students for this class
    class_students = db.query(models.Student).join(models.ClassStudent).filter(
        models.ClassStudent.clase_id == clase_id
    ).all()
    
    recognized_students = []
    
    for face in faces:
        aligned_face = face_recognizer.align_face(img, face['kps'])
        embedding = face_recognizer.get_embedding(aligned_face)
        
        if embedding is None:
            continue
            
        best_match = None
        max_similarity = 0.0
        threshold = 0.5 # Adjust as needed
        
        for student in class_students:
            if not student.embedding:
                continue
            
            try:
                student_emb = np.array(json.loads(student.embedding))
                sim = face_recognizer.compute_similarity(embedding, student_emb)
                
                if sim > max_similarity and sim > threshold:
                    max_similarity = sim
                    best_match = student
            except:
                continue
        
        if best_match:
            # Check if already marked present
            detail = db.query(models.AttendanceDetail).filter(
                models.AttendanceDetail.asistencia_id == attendance.id,
                models.AttendanceDetail.alumno_id == best_match.id
            ).first()
            
            if not detail:
                detail = models.AttendanceDetail(
                    asistencia_id=attendance.id,
                    alumno_id=best_match.id,
                    presente=True
                )
                db.add(detail)
                recognized_students.append(best_match)
    
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/{attendance_id}", response_model=schemas.AttendanceResponse)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance
