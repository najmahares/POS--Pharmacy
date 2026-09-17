from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    medical_record_number: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    allergies: Optional[str] = None
    loyalty_points: int = 0
    is_walk_in: bool = False
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    medical_record_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    allergies: Optional[str] = None
    loyalty_points: Optional[int] = None
    is_walk_in: Optional[bool] = None
    is_active: Optional[bool] = None


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
