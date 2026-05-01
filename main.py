from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from schemas import DoctorCreate, DoctorUpdate, DoctorResponse
from crud import get_doctor, get_doctors, create_doctor, update_doctor, delete_doctor

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doctor API",
    description="CRUD API for managing doctor records"
)

@app.post("/doctors", response_model=DoctorResponse)
def create_doctor_endpoint(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db=db, doctor=doctor)

@app.get("/doctors", response_model=list[DoctorResponse])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_doctors(db, skip=skip, limit=limit)

@app.get("/doctors/{doctor_id}", response_model=DoctorResponse)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = get_doctor(db, doctor_id=doctor_id)

    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return db_doctor

@app.put("/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor_endpoint(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db)
):
    return update_doctor(db=db, doctor_id=doctor_id, doctor_update=doctor)

@app.delete("/doctors/{doctor_id}")
def delete_doctor_endpoint(doctor_id: int, db: Session = Depends(get_db)):
    return delete_doctor(db=db, doctor_id=doctor_id)