from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import authenticate, register

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    return register(db, data)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate(db, form_data.username, form_data.password)
