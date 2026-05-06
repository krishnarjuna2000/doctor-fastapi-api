from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import create_patient, get_patients, get_patient_by_id, get_patients_for_doctor
from app.database import get_db
from app.auth.dependencies import require_admin, require_doctor_or_admin, get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=PatientResponse, dependencies=[Depends(require_admin)])
def create_patient_endpoint(patient_data: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db=db, patient_in=patient_data)


@router.get("/", response_model=List[PatientResponse])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(require_doctor_or_admin)):
    # Admin can see all patients, doctor can only see their own
    if current_user.role == "doctor" and current_user.doctor_id is not None:
        return get_patients_for_doctor(db=db, doctor_id=current_user.doctor_id)
    return get_patients(db=db, skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=PatientResponse)
def read_patient(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_doctor_or_admin)):
    patient = get_patient_by_id(db=db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Doctors can only view their assigned patients, admins can view all
    if current_user.role == "doctor" and current_user.doctor_id is not None:
        if current_user.doctor_id != patient.doctor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctors can only view their own patients")

    return patient
