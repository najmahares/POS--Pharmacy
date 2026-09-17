from datetime import date, datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., pattern=r"^(admin|pharmacist|pharmacy-technician|cashier|inventory-manager)$")
    license_number: Optional[str] = Field(None, max_length=50)
    license_expiry: Optional[date] = None
    department: Optional[str] = Field(None, max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = Field(None, pattern=r"^(admin|pharmacist|pharmacy-technician|cashier|inventory-manager)$")
    license_number: Optional[str] = Field(None, max_length=50)
    license_expiry: Optional[date] = None
    department: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]
