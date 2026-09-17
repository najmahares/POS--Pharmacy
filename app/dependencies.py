
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_user_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token."""
    return get_user_from_token(db, token)


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


def require_pharmacist(current_user: User = Depends(get_current_user)) -> User:
    """Require pharmacist role."""
    if current_user.role not in ["admin", "pharmacist"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pharmacist privileges required"
        )
    return current_user


def require_inventory_manager(current_user: User = Depends(get_current_user)) -> User:
    """Require inventory manager role."""
    if current_user.role not in ["admin", "inventory-manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inventory manager privileges required"
        )
    return current_user


def require_pharmacy_tech(current_user: User = Depends(get_current_user)) -> User:
    """Require pharmacy technician role."""
    if current_user.role not in ["admin", "pharmacist", "pharmacy-technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pharmacy technician privileges required"
        )
    return current_user

