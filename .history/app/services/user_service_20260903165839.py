from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, id: UUID):
    user = user_repository.get(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def list_users(db: Session):
    return user_repository.get_all(db)


def create_user(db: Session, data: UserCreate):
    return user_repository.create(db, data.model_dump())


def update_user(db: Session, id: UUID, data: UserUpdate):
    user = get_user(db, id)
    return user_repository.update(db, user, data.model_dump(exclude_unset=True))


def delete_user(db: Session, id: UUID):
    user = get_user(db, id)
    user_repository.delete(db, user)
