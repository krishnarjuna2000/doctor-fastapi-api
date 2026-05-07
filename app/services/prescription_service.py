from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.prescription import Prescription
from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse


def get_prescription(db: Session, prescription_id: int) -> Optional[Prescription]:
    """Get a single prescription by ID."""
    return db.query(Prescription).filter(Prescription.id == prescription_id).first()


def get_prescriptions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    appointment_id: Optional[int] = None
) -> List[Prescription]:
    """Get prescriptions with optional filtering."""
    query = db.query(Prescription)

    if doctor_id:
        query = query.filter(Prescription.doctor_id == doctor_id)
    if patient_id:
        query = query.filter(Prescription.patient_id == patient_id)
    if appointment_id:
        query = query.filter(Prescription.appointment_id == appointment_id)

    return query.offset(skip).limit(limit).all()


def create_prescription(db: Session, prescription: PrescriptionCreate, current_user_id: int) -> Prescription:
    """Create a new prescription with validation."""
    # Only doctors can create prescriptions
    doctor = db.query(Doctor).filter(Doctor.id == prescription.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Check if the doctor is creating for themselves
    if prescription.doctor_id != current_user_id:
        raise HTTPException(status_code=403, detail="Can only create prescriptions for own appointments")

    # Check if appointment exists and is completed
    appointment = db.query(Appointment).filter(Appointment.id == prescription.appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.status != AppointmentStatus.completed:
        raise HTTPException(
            status_code=400,
            detail="Prescription can only be created for completed appointments"
        )

    if appointment.doctor_id != prescription.doctor_id:
        raise HTTPException(status_code=403, detail="Appointment does not belong to this doctor")

    if appointment.patient_id != prescription.patient_id:
        raise HTTPException(status_code=400, detail="Patient does not match appointment")

    # Check if prescription already exists for this appointment
    existing = db.query(Prescription).filter(
        Prescription.appointment_id == prescription.appointment_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Prescription already exists for this appointment"
        )

    try:
        db_prescription = Prescription(**prescription.model_dump())
        db.add(db_prescription)
        db.commit()
        db.refresh(db_prescription)
        return db_prescription
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Prescription creation failed")


def update_prescription(
    db: Session,
    prescription_id: int,
    prescription_update: PrescriptionUpdate,
    current_user_id: int
) -> Prescription:
    """Update a prescription (only by the prescribing doctor)."""
    prescription = get_prescription(db, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    if prescription.doctor_id != current_user_id:
        raise HTTPException(status_code=403, detail="Can only update own prescriptions")

    update_data = prescription_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prescription, field, value)

    try:
        db.commit()
        db.refresh(prescription)
        return prescription
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Prescription update failed")


def delete_prescription(db: Session, prescription_id: int, current_user_id: int) -> Prescription:
    """Delete a prescription (only by the prescribing doctor)."""
    prescription = get_prescription(db, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    if prescription.doctor_id != current_user_id:
        raise HTTPException(status_code=403, detail="Can only delete own prescriptions")

    db.delete(prescription)
    db.commit()
    return prescription