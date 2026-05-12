from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.database import create_database_if_missing, engine, Base
from app.routers import auth as auth_router
from app.routers import doctors as doctor_router
from app.routers import patients as patient_router
from app.routers import appointments
from app.routers import prescriptions as prescription_router  # Added for Task 3

app = FastAPI(
    title="Doctor API",
    description="Production-style FastAPI backend for doctor and patient management with appointments and prescriptions",
    version="2.0.0"  # Updated version for Task 3
)


@app.on_event("startup")
def startup_event():
    """Initialize database when the app starts."""
    create_database_if_missing()
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized on startup")


@app.get("/", tags=["Root"])
def root():
    """Welcome endpoint - API information."""
    return {
        "message": "Welcome to Doctor API",
        "description": "A production-style FastAPI backend for doctor and patient management with appointments and prescriptions",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": {
            "authentication": "/auth/login, /auth/register",
            "doctors": "/doctors",
            "patients": "/patients",
            "appointments": "/appointments",  # Added for Task 3
            "prescriptions": "/prescriptions",  # Added for Task 3
            "health": "/health"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "API is running"
    }


@app.get("/favicon.ico", tags=["Root"])
def favicon():
    """Favicon endpoint - returns 204 No Content."""
    return JSONResponse(status_code=204)


app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(doctor_router.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patient_router.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(prescription_router.router, prefix="/prescriptions", tags=["Prescriptions"])  # Added for Task 3
