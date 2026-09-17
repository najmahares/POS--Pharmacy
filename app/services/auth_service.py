"""Authentication service module."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (create_access_token, create_refresh_token,
                               decode_access_token, hash_password, verify_hash)
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import TokenResponse, UserCreate


def register(db: Session, data: UserCreate) -> User:
    """Register a new user."""
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    if user_repository.get_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    values = data.model_dump(exclude={"password"})
    values["password_hash"] = hash_password(data.password)
    return user_repository.create(db, values)


def authenticate(db: Session, username: str, password: str) -> TokenResponse:
    """Authenticate a user and return tokens."""
    user = user_repository.get_by_username(db, username)
    if not user or not verify_hash(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive. Please contact administrator."
        )

    user.last_login = datetime.now()
    db.commit()
    db.refresh(user)

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=30 * 60,
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    )


def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
    """Refresh access token using refresh token."""
    try:
        try:
            _check = decode_access_token(refresh_token)
            if _check.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid refresh token")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        payload = decode_access_token(refresh_token)
        user_id = UUID(payload.get("sub"))
        user = user_repository.get(db, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        access_token = create_access_token(str(user.id))
        new_refresh_token = create_refresh_token(str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=30 * 60,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        ) from exc


def get_user_from_token(db: Session, token: str) -> User:
    """Get user from JWT token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject.strip():
            raise credentials_error

        try:
            user_id = UUID(subject)
        except ValueError as exc:
            raise credentials_error from exc

    except ValueError as e:
        if "Token has expired" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
        raise credentials_error from e
    except Exception as exc:
        raise credentials_error from exc

    user = user_repository.get(db, user_id)
    if user is None:
        raise credentials_error

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive",
        )
    return user
