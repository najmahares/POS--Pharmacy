from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import auth_service
from app.schemas.user import UserCreate, UserRead, TokenResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return auth_service.register(db, data)

@router.post("/login", response_model=TokenResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return auth_service.authenticate(db, form_data.username, form_data.password)

@router.post("/login/json", response_model=TokenResponse)
def login_user_json(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    return auth_service.authenticate(db, login_data.username, login_data.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    return auth_service.refresh_access_token(db, refresh_token)