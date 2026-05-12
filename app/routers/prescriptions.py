from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.auth.dependencies import get_current_user, require_doctor
from app.services.prescription_service import (
    get_prescription,
    get_prescriptions,
    create_prescription,
    update_prescription,
    delete_prescription
)
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse
)
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=PrescriptionResponse)
def create_new_prescription(
    prescription: PrescriptionCreate,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Create a new prescription. Only doctors can create prescriptions."""
    return create_prescription(db, prescription, current_user.doctor_id or current_user.id)


@router.get("/", response_model=List[PrescriptionResponse])
def read_prescriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    doctor_id: Optional[int] = Query(None, ge=1),
    patient_id: Optional[int] = Query(None, ge=1),
    appointment_id: Optional[int] = Query(None, ge=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get prescriptions with filtering. Role-based access control."""
    # Filter based on user role
    if current_user.role == "patient":
        # Patients can only see their own prescriptions
        patient_id = current_user.patient_id
    elif current_user.role == "doctor":
        # Doctors can see their own prescriptions
        doctor_id = current_user.doctor_id if current_user.doctor_id else current_user.id

    # Admin can see all prescriptions (no filtering)

    return get_prescriptions(
        db=db,
        skip=skip,
        limit=limit,
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_id=appointment_id
    )


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def read_prescription(
    prescription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific prescription by ID."""
    prescription = get_prescription(db, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    # Authorization checks
    if current_user.role == "patient" and prescription.patient_id != current_user.patient_id:
        raise HTTPException(status_code=403, detail="Can only view own prescriptions")
    elif current_user.role == "doctor" and prescription.doctor_id != current_user.doctor_id:
        raise HTTPException(status_code=403, detail="Can only view own prescriptions")

    # Admin can view any prescription
    return prescription


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_existing_prescription(
    prescription_id: int,
    prescription_update: PrescriptionUpdate,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Update a prescription. Only the prescribing doctor can update."""
    return update_prescription(
        db=db,
        prescription_id=prescription_id,
        prescription_update=prescription_update,
        current_user_id=current_user.doctor_id or current_user.id
    )


@router.delete("/{prescription_id}", response_model=PrescriptionResponse)
def delete_existing_prescription(
    prescription_id: int,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db)
):
    """Delete a prescription. Only the prescribing doctor can delete."""
    return delete_prescription(
        db=db,
        prescription_id=prescription_id,
        current_user_id=current_user.doctor_id or current_user.id
    )