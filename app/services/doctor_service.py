from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.doctor import DoctorCreate, DoctorUpdate


def get_doctor(db: Session, doctor_id: int) -> Optional[Doctor]:
    return db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.is_active.is_(True)).first()


def get_doctors(db: Session, skip: int = 0, limit: int = 100) -> List[Doctor]:
    return db.query(Doctor).filter(Doctor.is_active.is_(True)).offset(skip).limit(limit).all()


def create_doctor(db: Session, doctor_in: DoctorCreate) -> Doctor:
    doctor = Doctor(**doctor_in.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def update_doctor(db: Session, doctor_id: int, doctor_update: DoctorUpdate) -> Optional[Doctor]:
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    for field, value in doctor_update.dict(exclude_unset=True).items():
        setattr(doctor, field, value)
    db.commit()
    db.refresh(doctor)
    return doctor


def soft_delete_doctor(db: Session, doctor_id: int) -> Optional[Doctor]:
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    doctor.is_active = False
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctor_patients(db: Session, doctor_id: int):
    return db.query(Patient).filter(Patient.doctor_id == doctor_id).all()


def assign_patient_to_doctor(db: Session, doctor_id: int, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return None
    patient.doctor_id = doctor_id
    db.commit()
    db.refresh(patient)
    return patient
