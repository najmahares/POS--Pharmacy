"""User schema module."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=150)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(
        ...,
        pattern=r"^(admin|pharmacist|pharmacy-technician|cashier|inventory-manager)$",
    )
    license_number: str | None = Field(None, max_length=50)
    license_expiry: date | None = None
    department: str | None = Field(None, max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login schema."""

    username: str
    password: str


class UserUpdate(BaseModel):
    """User update schema."""

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = Field(None, max_length=150)
    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    role: str | None = Field(
        None,
        pattern=r"^(admin|pharmacist|pharmacy-technician|cashier|inventory-manager)$",
    )
    license_number: str | None = Field(None, max_length=50)
    license_expiry: date | None = None
    department: str | None = Field(None, max_length=100)
    is_active: bool | None = None
    password: str | None = Field(None, min_length=8)


class UserRead(UserBase):
    """User read schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict
