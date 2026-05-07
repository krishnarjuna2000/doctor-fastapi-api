from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, time, datetime
from enum import Enum


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str = Field(..., min_length=5, max_length=500)
    status: AppointmentStatus = AppointmentStatus.scheduled
    notes: Optional[str] = Field(None, max_length=1000)


class AppointmentCreate(AppointmentBase):
    @validator('appointment_date')
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError('Appointment date cannot be in the past')
        return v

    @validator('appointment_time')
    def validate_time(cls, v, values):
        if 'appointment_date' in values and values['appointment_date'] == date.today():
            # For today, time should be in the future
            now = datetime.now().time()
            if v <= now:
                raise ValueError('Appointment time must be in the future for today')
        return v


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    reason: Optional[str] = Field(None, min_length=5, max_length=500)
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)


class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True