from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date, time
from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse


def get_appointment(db: Session, appointment_id: int) -> Optional[Appointment]:
    """Get a single appointment by ID."""
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_appointments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    status: Optional[AppointmentStatus] = None,
    appointment_date: Optional[date] = None
) -> List[Appointment]:
    """Get appointments with optional filtering."""
    query = db.query(Appointment)

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if status:
        query = query.filter(Appointment.status == status)
    if appointment_date:
        query = query.filter(Appointment.appointment_date == appointment_date)

    return query.offset(skip).limit(limit).all()


def create_appointment(db: Session, appointment: AppointmentCreate) -> Appointment:
    """Create a new appointment with validation."""
    # Check if doctor exists and is active
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor is not active")

    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Check for overlapping appointments for the doctor
    overlapping = db.query(Appointment).filter(
        and_(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_date == appointment.appointment_date,
            Appointment.appointment_time == appointment.appointment_time,
            Appointment.status != AppointmentStatus.cancelled
        )
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Doctor already has an appointment at this date and time"
        )

    try:
        db_appointment = Appointment(**appointment.model_dump())
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Appointment creation failed")


def update_appointment(
    db: Session,
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    current_user
) -> Appointment:
    """Update an appointment with proper authorization."""
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Authorization checks
    if current_user.role == "patient":
        if appointment.patient_id != current_user.patient_id:
            raise HTTPException(status_code=403, detail="Can only update own appointments")
        # Patients can only cancel scheduled appointments
        if appointment_update.status and appointment_update.status != AppointmentStatus.cancelled:
            raise HTTPException(status_code=400, detail="Patients can only cancel appointments")
        if appointment.status != AppointmentStatus.scheduled:
            raise HTTPException(status_code=400, detail="Can only cancel scheduled appointments")

    elif current_user.role == "doctor":
        if appointment.doctor_id != current_user.doctor_id:
            raise HTTPException(status_code=403, detail="Can only update own appointments")
        # Doctors can update status for their appointments

    # Admin can update any appointment

    # Check for overlapping if date/time is being updated
    if appointment_update.appointment_date or appointment_update.appointment_time:
        new_date = appointment_update.appointment_date or appointment.appointment_date
        new_time = appointment_update.appointment_time or appointment.appointment_time

        overlapping = db.query(Appointment).filter(
            and_(
                Appointment.doctor_id == appointment.doctor_id,
                Appointment.appointment_date == new_date,
                Appointment.appointment_time == new_time,
                Appointment.id != appointment_id,
                Appointment.status != AppointmentStatus.cancelled
            )
        ).first()

        if overlapping:
            raise HTTPException(
                status_code=400,
                detail="Doctor already has an appointment at this date and time"
            )

    update_data = appointment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)

    try:
        db.commit()
        db.refresh(appointment)
        return appointment
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Appointment update failed")


def delete_appointment(db: Session, appointment_id: int, current_user) -> Appointment:
    """Soft delete (cancel) an appointment."""
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Authorization checks
    if current_user.role == "patient":
        if appointment.patient_id != current_user.patient_id:
            raise HTTPException(status_code=403, detail="Can only cancel own appointments")
        if appointment.status != AppointmentStatus.scheduled:
            raise HTTPException(status_code=400, detail="Can only cancel scheduled appointments")

    elif current_user.role == "doctor":
        if appointment.doctor_id != current_user.doctor_id:
            raise HTTPException(status_code=403, detail="Can only cancel own appointments")

    # Admin can cancel any appointment

    appointment.status = AppointmentStatus.cancelled
    db.commit()
    db.refresh(appointment)
    return appointment