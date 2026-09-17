
from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository class for User model operations."""

    def __init__(self):
        """Initialize UserRepository."""
        self.model = User

    def get(self, db: Session, user_id: UUID) -> Optional[User]:
        """Get a user by UUID."""
        return db.get(User, user_id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return db.query(User).offset(skip).limit(limit).all()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get a user by username."""
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, data: dict) -> User:
        """Create a new user."""
        obj = User(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: User, data: dict) -> User:
        """Update an existing user."""
        for field, value in data.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: User) -> None:
        """Delete a user."""
        db.delete(db_obj)
        db.commit()

    def update_last_login(self, db: Session, user_id: UUID) -> User:
        """Update user's last login timestamp."""
        from datetime import datetime
        user = self.get(db, user_id)
        if user:
            user.last_login = datetime.now()
            db.commit()
            db.refresh(user)
        return user


user_repository = UserRepository()