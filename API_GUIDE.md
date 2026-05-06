# Doctor API - Production Backend

A production-style FastAPI backend for managing doctors, patients, and authentication with role-based access control.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
Copy `.env.example` to `.env` and update MySQL credentials:
```bash
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=doctor_db
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Seed Database (Optional)
```bash
python seed.py
```

### 4. Run Server
```bash
uvicorn main:app --host 127.0.0.1 --port 8001
```

### 5. Access API
- **Swagger UI**: http://127.0.0.1:8001/docs
- **ReDoc**: http://127.0.0.1:8001/redoc
- **Health Check**: http://127.0.0.1:8001/health

---

## 📋 API Endpoints

### Health & Info
- `GET /` - Welcome & API info
- `GET /health` - Health check

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Doctors
- `POST /doctors` - Create doctor (Admin only)
- `GET /doctors` - List all doctors
- `GET /doctors/{id}` - Get doctor details
- `PUT /doctors/{id}` - Update doctor (Admin only)
- `DELETE /doctors/{id}` - Soft delete doctor (Admin only)

### Patients
- `POST /patients` - Create patient (Admin only)
- `GET /patients` - List patients (Admin: all, Doctor: own)
- `GET /patients/{id}` - Get patient details

### Doctor-Patient Assignment
- `POST /doctors/{doctor_id}/patients/{patient_id}` - Assign patient to doctor (Admin only)
- `GET /doctors/{doctor_id}/patients` - Get doctor's patients

---

## 🔐 Test Credentials

After running `seed.py`, use these credentials:

### Admin User
```
Email: admin@hospital.com
Password: admin123
```

### Doctor Users
```
doctor1@hospital.com / doctor1123
doctor2@hospital.com / doctor2123
doctor3@hospital.com / doctor3123
doctor4@hospital.com / doctor4123
```

---

## 📝 Example API Calls

### 1. Register a User
```bash
curl -X POST "http://127.0.0.1:8001/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. New User",
    "email": "newuser@hospital.com",
    "password": "password123",
    "role": "doctor",
    "doctor_id": 1
  }'
```

### 2. Login
```bash
curl -X POST "http://127.0.0.1:8001/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hospital.com",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create Doctor (Admin Only)
```bash
curl -X POST "http://127.0.0.1:8001/doctors" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Jane Doe",
    "email": "jane.doe@hospital.com",
    "specialization": "Dermatology",
    "phone": "+1-555-9999",
    "experience": 20,
    "is_active": true
  }'
```

### 4. Get All Doctors
```bash
curl -X GET "http://127.0.0.1:8001/doctors" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Create Patient (Admin Only)
```bash
curl -X POST "http://127.0.0.1:8001/patients" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Patient",
    "age": 35,
    "phone": "555-1234",
    "doctor_id": 1
  }'
```

### 6. Get Doctor's Patients
```bash
curl -X GET "http://127.0.0.1:8001/doctors/1/patients" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Assign Patient to Doctor
```bash
curl -X POST "http://127.0.0.1:8001/doctors/1/patients/5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🏗️ Project Structure

```
doctor_api/
├── app/
│   ├── __init__.py
│   ├── config.py                # Configuration management
│   ├── database.py              # Database connection
│   ├── main.py                  # FastAPI app setup
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── doctor.py            # Doctor model
│   │   └── patient.py           # Patient model
│   ├── schemas/
│   │   ├── auth.py              # Auth schemas
│   │   ├── user.py              # User schemas
│   │   ├── doctor.py            # Doctor schemas
│   │   └── patient.py           # Patient schemas
│   ├── services/
│   │   ├── user_service.py      # User operations
│   │   ├── doctor_service.py    # Doctor operations
│   │   └── patient_service.py   # Patient operations
│   ├── auth/
│   │   ├── utils.py             # JWT & password hashing
│   │   └── dependencies.py      # Auth dependencies
│   └── routers/
│       ├── auth.py              # Auth routes
│       ├── doctors.py           # Doctor routes
│       └── patients.py          # Patient routes
├── main.py                      # App entry point
├── seed.py                      # Database seeding script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── .env.example                 # Example env file
```

---

## 🔒 Authentication Flow

1. User registers via `/auth/register` or logs in via `/auth/login`
2. Server returns JWT token (valid for 60 minutes by default)
3. Include token in `Authorization: Bearer <token>` header for protected routes
4. Server validates token and extracts user info
5. Role-based access is enforced:
   - **Admin**: Can manage all doctors and patients
   - **Doctor**: Can view only assigned patients

---

## 🛡️ Features

✅ JWT Authentication  
✅ Password hashing with bcrypt  
✅ Role-based access control (Admin/Doctor)  
✅ User registration & login  
✅ Doctor management (CRUD + soft delete)  
✅ Patient management  
✅ Doctor-patient assignment  
✅ MySQL integration  
✅ Pydantic v2 validation  
✅ Comprehensive error handling  
✅ Swagger/OpenAPI documentation  

---

## 📦 Dependencies

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **MySQL/PyMySQL** - Database
- **PyJWT** - JWT tokens
- **bcrypt** - Password hashing
- **python-dotenv** - Environment variables

---

## 🐛 Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check credentials in `.env`
- Verify database name

### Port Already in Use
```bash
uvicorn main:app --port 8002  # Use different port
```

### Permission Denied
- Ensure you're logged in as Admin for protected routes
- Check JWT token validity

---

## 📄 License

MIT License - feel free to use and modify!
