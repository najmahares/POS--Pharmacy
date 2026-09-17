from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[UserRead])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    return user_repository.get_all(db, skip, limit)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    return user_repository.create(db, data.model_dump())

@router.get("/me", response_model=UserRead)
def get_me(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, data: UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_repository.update(db, user, data.model_dump(exclude_unset=True))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_repository.delete(db, user)
