from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class PatientBase(BaseModel):
    name: str
    age: int
    phone: str

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError("Age must be greater than zero")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        digits = [ch for ch in value if ch.isdigit()]
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Phone number must have 10 to 15 digits")
        return value


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    doctor_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True