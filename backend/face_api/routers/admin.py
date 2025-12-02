from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import sql_models as models
from ..schemas import user as schemas

router = APIRouter(
    prefix="/admins",
    tags=["admins"]
)

@router.post("/", response_model=schemas.AdminResponse)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(models.Admin).filter(models.Admin.correo == admin.correo).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_hashed_password = admin.password + "notreallyhashed" # TODO: Hash password
    new_admin = models.Admin(nombre=admin.nombre, correo=admin.correo, password=fake_hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@router.get("/", response_model=List[schemas.AdminResponse])
def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    admins = db.query(models.Admin).offset(skip).limit(limit).all()
    return admins
