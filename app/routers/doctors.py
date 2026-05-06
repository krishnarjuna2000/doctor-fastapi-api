from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from app.services.doctor_service import (
    get_doctors,
    get_doctor,
    create_doctor,
    update_doctor,
    soft_delete_doctor,
    assign_patient_to_doctor,
    get_doctor_patients,
)
from app.database import get_db
from app.auth.dependencies import require_admin, require_doctor_or_admin, get_current_user
from app.models.user import User
from app.schemas.patient import PatientResponse

router = APIRouter()


@router.post("/", response_model=DoctorResponse, dependencies=[Depends(require_admin)])
def create_doctor_endpoint(doctor_data: DoctorCreate, db: Session = Depends(get_db)):
    try:
        return create_doctor(db=db, doctor_in=doctor_data)
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A doctor with this email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error: " + str(e)
        )


@router.get("/", response_model=List[DoctorResponse], dependencies=[Depends(get_current_user)])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_doctors(db=db, skip=skip, limit=limit)


@router.get("/{doctor_id}", response_model=DoctorResponse, dependencies=[Depends(get_current_user)])
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = get_doctor(db=db, doctor_id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return doctor


@router.put("/{doctor_id}", response_model=DoctorResponse, dependencies=[Depends(require_admin)])
def update_doctor_endpoint(doctor_id: int, doctor_data: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = update_doctor(db=db, doctor_id=doctor_id, doctor_update=doctor_data)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return doctor


@router.delete("/{doctor_id}", dependencies=[Depends(require_admin)])
def delete_doctor_endpoint(doctor_id: int, db: Session = Depends(get_db)):
    doctor = soft_delete_doctor(db=db, doctor_id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return {"detail": "Doctor soft deleted successfully."}


@router.post("/{doctor_id}/patients/{patient_id}", response_model=PatientResponse, dependencies=[Depends(require_admin)])
def assign_patient(doctor_id: int, patient_id: int, db: Session = Depends(get_db)):
    patient = assign_patient_to_doctor(db=db, doctor_id=doctor_id, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


@router.get("/{doctor_id}/patients", response_model=List[PatientResponse])
def read_doctor_patients(doctor_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_doctor_or_admin)):
    # Doctors can only view their own patients, admins can view all
    if current_user.role == "doctor" and current_user.doctor_id is not None:
        if current_user.doctor_id != doctor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctors can only view their own patients")
    return get_doctor_patients(db=db, doctor_id=doctor_id)
