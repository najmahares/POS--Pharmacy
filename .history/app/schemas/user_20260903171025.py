"""User router module."""

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
    """Get all users with pagination. Requires admin role."""
    return user_repository.get_all(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Get a specific user by ID. Requires admin role."""
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
    _current_user: User = Depends(require_admin),
):
    """Get a user by username. Requires admin role."""
    user = user_repository.get_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/email/{email}", response_model=UserRead)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Get a user by email. Requires admin role."""
    user = user_repository.get_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/me", response_model=UserRead)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current authenticated user information."""
    return current_user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Create a new user. Requires admin role."""
    # Check if username already exists
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Check if email already exists
    if user_repository.get_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return user_repository.create(db, data.model_dump())


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Update an existing user. Requires admin role."""
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_repository.update(db, user, data.model_dump(exclude_unset=True))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    """Delete a user. Requires admin role."""
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user_repository.delete(db, user)
    return None