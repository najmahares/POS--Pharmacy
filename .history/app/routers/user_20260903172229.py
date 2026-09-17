from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    return user_repository.get_all(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/username/{username}", response_model=UserRead)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    _current_user: User = Dep