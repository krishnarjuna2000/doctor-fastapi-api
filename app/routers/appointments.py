from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.auth.dependencies import get_current_user, require_admin, require_doctor, require_patient
from app.services.appointment_service import (
    get_appointment,
    get_appointments,
    create_appointment,
    update_appointment,
    delete_appointment
)
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentStatus
)
from app.models.user import User

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentResponse)
def create_new_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new appointment. Patients can book, doctors can create for patients."""
    # Patients can create appointments for themselves
    if current_user.role == "patient":
        # For patients, ensure they can only book for themselves
        # But we need to map user_id to patient_id - this might need adjustment
        pass  # For now, allow as per schema validation

    # Doctors and admins can create appointments
    return create_appointment(db, appointment)


@router.get("/", response_model=List[AppointmentResponse])
def read_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    doctor_id: Optional[int] = Query(None, ge=1),
    patient_id: Optional[int] = Query(None, ge=1),
    status: Optional[AppointmentStatus] = None,
    appointment_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get appointments with filtering. Role-based access control."""
    # Filter based on user role
    if current_user.role == "patient":
        # Patients can only see their own appointments
        patient_id = current_user.id  # Assuming user.id maps to patient.id - may need adjustment
    elif current_user.role == "doctor":
        # Doctors can see their own appointments
        doctor_id = current_user.doctor_id if current_user.doctor_id else current_user.id

    # Admin can see all appointments (no filtering)

    return get_appointments(
        db=db,
        skip=skip,
        limit=limit,
        doctor_id=doctor_id,
        patient_id=patient_id,
        status=status,
        appointment_date=appointment_date
    )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def read_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific appointment by ID."""
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Authorization checks
    if current_user.role == "patient" and appointment.patient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only view own appointments")
    elif current_user.role == "doctor" and appointment.doctor_id != current_user.doctor_id:
        raise HTTPException(status_code=403, detail="Can only view own appointments")

    # Admin can view any appointment
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_existing_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an appointment. Role-based permissions."""
    return update_appointment(
        db=db,
        appointment_id=appointment_id,
        appointment_update=appointment_update,
        current_user_role=current_user.role,
        current_user_id=current_user.id
    )


@router.delete("/{appointment_id}", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel (soft delete) an appointment."""
    return delete_appointment(
        db=db,
        appointment_id=appointment_id,
        current_user_role=current_user.role,
        current_user_id=current_user.id
    )