from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PrescriptionBase(BaseModel):
    appointment_id: int
    doctor_id: int
    patient_id: int
    diagnosis: str = Field(..., min_length=5, max_length=500)
    medicines: str = Field(..., min_length=5)  # JSON string or comma-separated list
    dosage_instructions: str = Field(..., min_length=10)
    remarks: Optional[str] = Field(None, max_length=1000)


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionUpdate(BaseModel):
    diagnosis: Optional[str] = Field(None, min_length=5, max_length=500)
    medicines: Optional[str] = Field(None, min_length=5)
    dosage_instructions: Optional[str] = Field(None, min_length=10)
    remarks: Optional[str] = Field(None, max_length=1000)


class PrescriptionResponse(PrescriptionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True