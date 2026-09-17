from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List
from app.models.user import User

class UserRepository:
    def __init__(self):
        self.model = User

    def get(self, db: Session, id: UUID) -> Optional[User]:
        return db.get(User, id)
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_license_number(self, db: Session, license_number: str) -> Optional[User]:
        return db.query(User).filter(User.license_number == license_number).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict) -> User:
        obj = User(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, db_obj: User, data: dict) -> User:
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: User) -> None:
        db.delete(db_obj)
        db.commit()

user_repository = UserRepository()