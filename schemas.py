from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class DoctorBase(BaseModel):
    name: str
    email: EmailStr
    specialization: str
    phone: str
    experience: int
    is_active: Optional[bool] = True

    @validator('experience')
    def experience_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Experience must be >= 0')
        return v

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    experience: Optional[int] = None
    is_active: Optional[bool] = None

    @validator('experience')
    def experience_must_be_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('Experience must be >= 0')
        return v

class DoctorResponse(DoctorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True