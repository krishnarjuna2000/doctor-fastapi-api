# Project Structure Documentation

## 📦 Final Clean Project Structure

```
doctor_api/
│
├── app/                                  # Main application package
│   ├── __init__.py
│   ├── main.py                          # FastAPI app factory (startup events, routes inclusion)
│   ├── config.py                        # Configuration & environment variables
│   ├── database.py                      # SQLAlchemy engine, session, Base (SINGLE SOURCE OF TRUTH)
│   │
│   ├── auth/                            # Authentication & Authorization
│   │   ├── utils.py                     # JWT token generation, password hashing (bcrypt)
│   │   └── dependencies.py              # get_current_user, require_admin, require_doctor_or_admin
│   │
│   ├── models/                          # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── user.py                      # User model (admin/doctor roles)
│   │   ├── doctor.py                    # Doctor model (specialization, experience, etc)
│   │   └── patient.py                   # Patient model (name, age, phone, doctor_id FK)
│   │
│   ├── schemas/                         # Pydantic v2 Data Validation
│   │   ├── __init__.py
│   │   ├── auth.py                      # UserRegister, UserLogin (field validators)
│   │   ├── user.py                      # User response schemas
│   │   ├── doctor.py                    # DoctorCreate, DoctorUpdate, DoctorResponse
│   │   └── patient.py                   # PatientCreate, PatientUpdate, PatientResponse
│   │
│   ├── services/                        # Business Logic Layer
│   │   ├── user_service.py              # create_user, authenticate_user functions
│   │   ├── doctor_service.py            # Doctor CRUD + patient assignment
│   │   └── patient_service.py           # Patient CRUD operations
│   │
│   └── routers/                         # API Route Handlers
│       ├── __init__.py
│       ├── auth.py                      # POST /auth/register, POST /auth/login
│       ├── doctors.py                   # Doctor endpoints (POST, GET, PUT, DELETE)
│       └── patients.py                  # Patient endpoints (POST, GET, PUT, DELETE)
│
├── main.py                              # Lightweight entry point (imports app.main.app)
├── seed.py                              # Database seeding with sample data
├── test_api.py                          # Comprehensive test suite (11+ endpoints)
│
├── requirements.txt                     # Python dependencies
├── .env                                 # Environment variables (local, NEVER commit)
├── .env.example                         # Template for environment variables
├── .gitignore                           # Git ignore rules
│
├── README.md                            # Project overview & setup guide
├── API_GUIDE.md                         # Detailed API documentation with examples
└── PROJECT_STRUCTURE.md                 # This file

### Screenshot Directories (for documentation)
├── Screenshots task 1/                  # Original Task 1 implementation screenshots
└── ScreenShots T2/                      # Task 2 production features screenshots
```

---

## 🏗️ Architecture Layers

### 1. **Entry Point Layer** (`main.py`)
- Single lightweight entry point
- Imports FastAPI app from `app.main`
- Runs with: `python main.py` or `uvicorn main:app --reload`

### 2. **Application Layer** (`app/main.py`)
- FastAPI application factory
- Includes all routers (auth, doctors, patients)
- Startup event for database initialization
- Root endpoints: `/`, `/health`, `/docs`, `/swagger`

### 3. **Configuration Layer** (`app/config.py`)
- Environment variables management
- Database URL construction
- JWT configuration

### 4. **Database Layer** (`app/database.py`)
- SQLAlchemy engine setup
- Session factory
- Base class for models
- Database creation logic

### 5. **Model Layer** (`app/models/`)
- SQLAlchemy ORM models
- Database table definitions
- Relationships between entities
- **Models**: User, Doctor, Patient

### 6. **Validation Layer** (`app/schemas/`)
- Pydantic v2 schemas
- Request/response validation
- Field validators for business logic
- **Schemas**: Auth, User, Doctor, Patient

### 7. **Business Logic Layer** (`app/services/`)
- User creation and authentication
- Doctor CRUD and patient assignment
- Patient CRUD operations
- Encapsulates all business rules

### 8. **Authentication Layer** (`app/auth/`)
- JWT token creation/decoding
- Password hashing with bcrypt
- Authorization dependencies
- Role-based access control

### 9. **Route Handler Layer** (`app/routers/`)
- API endpoint definitions
- HTTP method handlers
- Route-specific validation
- Error response formatting
- **Routers**: Auth, Doctors, Patients

---

## 🔄 Data Flow Diagram

```
HTTP Request
    ↓
Router (app/routers/*.py)
    ↓
Schema Validation (app/schemas/*.py)
    ↓
Auth Check (app/auth/dependencies.py)
    ↓
Business Logic (app/services/*.py)
    ↓
Database Query (app/models/*.py)
    ↓
SQLAlchemy ORM (app/database.py)
    ↓
MySQL Database
    ↓
Response → HTTP Response
```

---

## 📊 Database Models

### User Model
```python
- id: int (PK)
- email: str (unique)
- hashed_password: str
- full_name: str
- role: str (admin/doctor)
- created_at: datetime
```

### Doctor Model
```python
- id: int (PK)
- name: str
- email: str (unique)
- specialization: str
- phone: str
- experience: int
- is_active: bool
- created_at: datetime
- user_id: int (FK)
```

### Patient Model
```python
- id: int (PK)
- name: str
- age: int
- phone: str
- condition: str
- doctor_id: int (FK)
- created_at: datetime
```

---

## 🔐 Authentication & Authorization

### JWT Flow
1. User registers → `POST /auth/register` (creates User with hashed password)
2. User login → `POST /auth/login` (validates credentials, returns JWT token)
3. Client includes token → `Authorization: Bearer <token>`
4. Dependency `get_current_user()` validates token and extracts user info
5. Role-based access → `require_admin()` or `require_doctor_or_admin()`

### Roles & Permissions
- **Admin**: Full access to doctor and patient management
- **Doctor**: Can view own patients, assign new patients, manage own patient records

---

## 📚 API Endpoints Summary

| Method | Endpoint | Role Required | Description |
|--------|----------|----------------|-------------|
| POST | `/auth/register` | None | Register new user |
| POST | `/auth/login` | None | Login and get JWT token |
| POST | `/doctors` | Admin | Create new doctor |
| GET | `/doctors` | Admin | Get all doctors |
| GET | `/doctors/{id}` | Auth | Get doctor details |
| PUT | `/doctors/{id}` | Admin | Update doctor |
| DELETE | `/doctors/{id}` | Admin | Delete doctor |
| POST | `/patients` | Auth | Create patient |
| GET | `/patients` | Auth | Get patients (filtered by role) |
| GET | `/patients/{id}` | Auth | Get patient details |
| PUT | `/patients/{id}` | Auth | Update patient |
| DELETE | `/patients/{id}` | Auth | Delete patient |
| POST | `/patients/{id}/assign-doctor` | Auth | Assign doctor to patient |

---

## 🧪 Testing

### Test Suite (`test_api.py`)
- Comprehensive test coverage
- Tests all 11+ endpoints
- Includes authentication flow
- Tests authorization (admin vs doctor)
- Error handling validation
- Sample data seeding

### Running Tests
```bash
python test_api.py
```

### Database Seeding
```bash
python seed.py
```

Populates with:
- 1 Admin user (admin@hospital.com)
- 1 Doctor user (doctor1@hospital.com)
- 4 pre-configured doctors
- 8 pre-configured patients

---

## 🛠️ Development Workflow

### Setup
```bash
# Clone repository
git clone https://github.com/krishnarjuna2000/doctor-fastapi-api.git
cd doctor_api

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials
```

### Development
```bash
# Run the application
python main.py

# Access API documentation
http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (ReDoc)

# Run tests
python test_api.py

# Seed database
python seed.py
```

### Deployment
```bash
# Production-ready server
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Design Principles Applied

1. **Single Responsibility Principle (SRP)**
   - Each module/file has one reason to change
   - Routers handle HTTP, services handle logic, models handle data

2. **Dependency Injection**
   - FastAPI dependencies for authentication
   - Loose coupling between components

3. **DRY (Don't Repeat Yourself)**
   - Centralized database configuration
   - Reusable service functions
   - Common auth logic in dependencies

4. **Separation of Concerns**
   - Models: Data representation
   - Schemas: Data validation
   - Services: Business logic
   - Routers: HTTP handling
   - Auth: Security logic

5. **Production-Ready Structure**
   - Proper error handling
   - Input validation
   - Security best practices
   - Comprehensive logging ready

---

## ✅ Quality Checklist

- ✅ No duplicate files (Task 1 & Task 2 merged)
- ✅ No duplicate models
- ✅ No duplicate database configs
- ✅ No duplicate CRUD logic
- ✅ Single FastAPI app instance
- ✅ Clean project structure
- ✅ All imports correct
- ✅ All endpoints working
- ✅ Authentication working
- ✅ Authorization working (RBAC)
- ✅ Test suite passing
- ✅ Database seeding working
- ✅ API documentation complete
- ✅ Beginner-friendly layout
- ✅ Production-quality code
- ✅ Interview-ready codebase

---

## 📝 Files Removed (Task 1 Duplicates)

These files were safely removed after consolidation:
- `database.py` (root) → `app/database.py`
- `models.py` (root) → `app/models/`
- `schemas.py` (root) → `app/schemas/`
- `crud.py` (root) → `app/services/`
- `DB_SETUP.md` (outdated)

---

## 🔗 Related Documentation

- [README.md](README.md) - Project overview and setup
- [API_GUIDE.md](API_GUIDE.md) - Detailed API documentation with examples

---

**Last Updated**: May 7, 2026
**Status**: ✅ Production-Ready
**Version**: 2.0 (Task 1 + Task 2 merged & refactored)
