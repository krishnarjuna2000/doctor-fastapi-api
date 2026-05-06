"""
Seed script to populate the database with dummy data.
Run: python seed.py
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, create_database_if_missing, engine, Base
from app.models.doctor import Doctor
from app.models.user import User
from app.models.patient import Patient
from app.auth.utils import hash_password

def clear_database():
    """Clear all tables."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✓ Database cleared and recreated")

def seed_database():
    """Populate database with dummy data."""
    create_database_if_missing()
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Patient).delete()
        db.query(User).delete()
        db.query(Doctor).delete()
        db.commit()
        
        # Create dummy doctors
        doctors_data = [
            {
                "name": "Dr. John Smith",
                "email": "john.smith@hospital.com",
                "specialization": "Cardiology",
                "phone": "+1-555-0101",
                "experience": 15
            },
            {
                "name": "Dr. Sarah Johnson",
                "email": "sarah.johnson@hospital.com",
                "specialization": "Neurology",
                "phone": "+1-555-0102",
                "experience": 12
            },
            {
                "name": "Dr. Michael Chen",
                "email": "michael.chen@hospital.com",
                "specialization": "Orthopedics",
                "phone": "+1-555-0103",
                "experience": 10
            },
            {
                "name": "Dr. Emily Davis",
                "email": "emily.davis@hospital.com",
                "specialization": "Pediatrics",
                "phone": "+1-555-0104",
                "experience": 8
            },
        ]
        
        doctors = []
        for doc_data in doctors_data:
            doctor = Doctor(**doc_data, is_active=True)
            db.add(doctor)
            doctors.append(doctor)
        
        db.commit()
        print(f"✓ Created {len(doctors)} doctors")
        
        # Create dummy admin user
        admin_user = User(
            name="Admin User",
            email="admin@hospital.com",
            password_hash=hash_password("admin123"),
            role="admin",
            doctor_id=None
        )
        db.add(admin_user)
        db.commit()
        print("✓ Created admin user (admin@hospital.com / admin123)")
        
        # Create dummy doctor users
        for i, doctor in enumerate(doctors):
            doctor_user = User(
                name=f"Dr. User {i+1}",
                email=f"doctor{i+1}@hospital.com",
                password_hash=hash_password(f"doctor{i+1}123"),
                role="doctor",
                doctor_id=doctor.id
            )
            db.add(doctor_user)
        
        db.commit()
        print(f"✓ Created {len(doctors)} doctor users")
        
        # Create dummy patients
        patients_data = [
            {"name": "John Doe", "age": 45, "phone": "5550201234", "doctor_id": doctors[0].id},
            {"name": "Jane Smith", "age": 32, "phone": "5550202345", "doctor_id": doctors[0].id},
            {"name": "Robert Johnson", "age": 58, "phone": "5550203456", "doctor_id": doctors[1].id},
            {"name": "Maria Garcia", "age": 28, "phone": "5550204567", "doctor_id": doctors[1].id},
            {"name": "David Lee", "age": 67, "phone": "5550205678", "doctor_id": doctors[2].id},
            {"name": "Lisa Wong", "age": 41, "phone": "5550206789", "doctor_id": doctors[2].id},
            {"name": "Michael Brown", "age": 5, "phone": "5550207890", "doctor_id": doctors[3].id},
            {"name": "Emma Wilson", "age": 8, "phone": "5550208901", "doctor_id": doctors[3].id},
        ]
        
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            db.add(patient)
        
        db.commit()
        print(f"✓ Created {len(patients_data)} patients")
        
        print("\n" + "="*60)
        print("DUMMY DATA SEEDING COMPLETE")
        print("="*60)
        print("\nTest Credentials:")
        print("  Admin:")
        print("    Email: admin@hospital.com")
        print("    Password: admin123")
        print("\n  Doctors:")
        for i in range(1, len(doctors) + 1):
            print(f"    Email: doctor{i}@hospital.com")
            print(f"    Password: doctor{i}123")
        print("\n" + "="*60)
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
