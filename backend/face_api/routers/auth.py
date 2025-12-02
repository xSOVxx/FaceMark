from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import sql_models as models
from ..utils import auth

router = APIRouter(
    tags=["auth"]
)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check Admin
    user = db.query(models.Admin).filter(models.Admin.correo == form_data.username).first()
    if not user:
        # Check Professor
        user = db.query(models.Professor).filter(models.Professor.correo == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password (using fake hash for now as per previous implementation)
    # In real app, use auth.verify_password(form_data.password, user.password)
    # Since we stored "notreallyhashed", we check that.
    if user.password != form_data.password + "notreallyhashed":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.correo}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
