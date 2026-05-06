from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate


def create_patient(db: Session, patient_in: PatientCreate) -> Patient:
    patient = Patient(**patient_in.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()


def get_patient_by_id(db: Session, patient_id: int) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patients_for_doctor(db: Session, doctor_id: int) -> List[Patient]:
    return db.query(Patient).filter(Patient.doctor_id == doctor_id).all()
