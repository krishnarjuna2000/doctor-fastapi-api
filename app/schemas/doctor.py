from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class DoctorBase(BaseModel):
    name: str
    email: EmailStr
    specialization: str
    phone: str
    experience: int
    is_active: Optional[bool] = True

    @field_validator("experience")
    @classmethod
    def experience_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError("Experience must be greater than or equal to 0")
        return value


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    experience: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator("experience")
    @classmethod
    def experience_must_be_non_negative(cls, value):
        if value is not None and value < 0:
            raise ValueError("Experience must be greater than or equal to 0")
        return value


class DoctorResponse(DoctorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
