"""User service module."""

from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: UUID):
    """Get a user by ID."""
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def list_users(db: Session):
    """List all users."""
    return user_repository.get_all(db)


def create_user(db: Session, data: UserCreate):
    """Create a new user."""
    return user_repository.create(db, data.model_dump())


def update_user(db: Session, user_id: UUID, data: UserUpdate):
    """Update an existing user."""
    user = get_user(db, user_id)
    return user_repository.update(db, user, data.model_dump(exclude_unset=True))


def delete_user(db: Session, user_id: UUID):
    """Delete a user."""
    user = get_user(db, user_id)
    user_repository.delete(db, user)